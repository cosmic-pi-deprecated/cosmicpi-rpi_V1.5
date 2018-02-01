'''
This program will check the database about every minute to search for a new event.
If one is found it will be sent to an mqtt server

'''


import time
import sqlite3
import configparser
import random
import json
import subprocess

import logging as log
log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO)


def _initilize_DB(_sqlite_location):
    _db_conn = sqlite3.connect(_sqlite_location, timeout=60.0)
    cursor = _db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Events'")
    if cursor.fetchone() == None:
        cursor.execute('''CREATE TABLE Events
         (UTCUnixTime INTEGER, SubSeconds REAL, TemperatureC REAL, Humidity REAL, AccelX REAL,
          AccelY REAL, AccelZ REAL, MagX REAL, MagY REAL, MagZ REAL, Pressure REAL, Longitude REAL,
          Latitude REAL, DetectorName TEXT, DetectorVersion TEXT);''')
        _db_conn.commit()


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial

def send_via_mqtt(broker_address, broker_topic, message):
    execution_string = "mosquitto_pub -h {} -t '{}' -m '{}'".format(broker_address, broker_topic, message)
    log.debug("Executing the following: {}".format(execution_string))
    # ToDo: This is unsafe, change it!
    subprocess.call(execution_string, shell=True)

# settings files
CONFIG_FILE = "../config/CosmicPi.config"

# read configuration
# Todo: Put the config parser into a propper class
# Todo: Implement proper error catching for configparser (e.g. non existent keys or file)
# read configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
sqlite_location = config.get("Storage", "sqlite_location")
broker_address = config.get("MQTT", "broker_address")
broker_topic = "{}/{}".format(config.get("MQTT", "broker_topic"), getserial())
last_sent_event_timestamp = 0


# setup the program
_initilize_DB(sqlite_location)

# start the cleaning loop
while(True):
    global last_sent_event_timestamp
    # establish a connection
    db_conn = sqlite3.connect(sqlite_location, timeout=60.0)
    # we would like to be able to use have our rows as dictionaries
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()

    # get the most recent time
    cursor.execute("SELECT * FROM Events ORDER BY UTCUnixTime DESC, SubSeconds DESC;")
    time_row = cursor.fetchone()
    # ToDo: Popper protection against an empty DB, this isn't working for some reason, but systemd will restart the program, so it's not completly deadly...
    if time_row == type(None):
        log.info("Got a none type, retrying in a bit")
        # sleep for a semi random time
        time_to_wait = int(random.randrange(30, 90))
        log.info("Sleeping for: {} [s]".format(time_to_wait))
        time.sleep(time_to_wait)
        continue
    latest_time = time_row[0]

    # Get the next events that will be sent
    cursor.execute("SELECT * FROM Events WHERE UTCUnixTime > ?;", (last_sent_event_timestamp,))
    # send the next events
    available_events = cursor.fetchall()
    log.info("Searched for events since: {}; Found the following number of new events: {}".format(last_sent_event_timestamp, len(available_events)))
    for event in available_events:
        message = json.dumps(dict(event))
        send_via_mqtt(broker_address, broker_topic, message)
    db_conn.close()

    # save the event time
    last_sent_event_timestamp = latest_time

    # sleep for a semi random time
    time_to_wait = int(random.randrange(1, 5))
    log.info("Sleeping for: {} [s]".format(time_to_wait))
    time.sleep(time_to_wait)
