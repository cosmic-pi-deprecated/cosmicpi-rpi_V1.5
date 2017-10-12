'''
This program manages the connection to an attached detector.

Features:
    Configurable via ../config/detector.config
    Start and/or setup the selected detector
    Calibrate selected detector
    Store event and sensor data in an sqlite data base

This program uses the interface of the class detector.
Thus, new detectors should be added via subclassing detector.

'''
config_sqlite_location = "../storage/sqlite_db"

import serial
import time
import threading
import sqlite3
import copy
import datetime



class detector():
    # vars that are the same for all detectors
    _db_keys = ["UTCUnixTime", "SubSeconds", "TemperatureC", "Humidity",
                     "AccelX", "AccelY", "AccelZ", "MagX", "MagY", "MagZ",
                     "Pressure", "Longitude", "Latitude"]
    _example_event_dict = {
        "UTCUnixTime": 0,
        "SubSeconds": 0.0,
        "TemperatureC": 0.0,
        "Humidity": 0.0,
        "AccelX": 0.0,
        "AccelY": 0.0,
        "AccelZ": 0.0,
        "MagX": 0.0,
        "MagY": 0.0,
        "MagZ": 0.0,
        "Pressure": 0.0,
        "Longitude": 0.0,
        "Latitude": 0.0
    }

    def __init__(self, detector_name, detector_version, sqlite_location):
        # vars local to one detector
        self._sqlite_location = sqlite_location
        self.detector_name = detector_name
        self.detector_version = detector_version
        self._read_out_lock = threading.Lock()
        self._db_conn = 0
        self._initilize_DB()
        self._detector_initilized = False

    def _initilize_DB(self):
        self._db_conn = sqlite3.connect(self._sqlite_location)
        cursor = self._db_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Events'")
        if cursor.fetchone() == None:
            cursor.execute('''CREATE TABLE Events
             (UTCUnixTime INTEGER, SubSeconds REAL, TempreatureC REAL, Humidity REAL, AccelX REAL,
              AccelY REAL, AccelZ REAL, MagX REAL, MagY REAL, MagZ REAL, Pressure REAL, Longitude REAL,
              Latitude REAL, DetectorName TEXT, DetectorVersion TEXT);''')
            self._db_conn.commit()

    def initzilize_detector(self):
        raise NotImplementedError("Should be implemented in the subclass!")

    def start(self):
        raise NotImplementedError("Should be implemented in the subclass!")

    def stop(self):
        raise NotImplementedError("Should be implemented in the subclass!")

    def _commit_event_dict(self, event_dict):
        cursor = self._db_conn.cursor()
        # compile what needs to be sent
        insert_vals = []
        insert_string = 'INSERT INTO Events VALUES (?,?'
        for key in self._db_keys:
            insert_vals.append(event_dict[key])
            insert_string += ',?'
        insert_string += ')'
        insert_vals.append(self.detector_name)
        insert_vals.append(self.detector_version)

        # send and commit the changes
        cursor.execute(insert_string, insert_vals)
        self._db_conn.commit()



class CosmicPi_V15(detector, threading.Thread):
    def __init__(self, serial_port, baud_rate, sqlite_location, timeout=10, raw_output_file=''):
        detector.__init__(self, "CosmicPi V1.5", "1.5.1", sqlite_location)
        # todo: put the thread inheritance one higher
        threading.Thread.__init__(self)
        # init vars
        self._gps_ok = False
        # start the detector
        self._output_file = raw_output_file
        self._event_dict = copy.deepcopy(self._example_event_dict)
        self._event_dict_confirmed = copy.deepcopy(self._example_event_dict)
        self._event_dict_confirmed.pop('SubSeconds')
        self._all_data_collected = False
        self._time_from_gps = datetime.datetime(2000, 1, 2, 3, 4, 5, tzinfo=None)
        # empty the output file on boot
        if self._output_file is not '':
            with open(self._output_file, 'w') as f:
                f.write(" ")
        self.ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

    def initzilize_detector(self):
        pass # nothing to do here (yet)

    def start(self):
        # make sure we empty the confirmations, to force new ones
        for element in self._event_dict_confirmed:
            self._event_dict_confirmed[element] = False
        self._gps_ok = False
        self.run()

    def stop(self):
        # could be implemented like this: https://stackoverflow.com/a/15734837
        raise NotImplementedError("Should be implemented in the subclass!")

    def run(self):
        # create an artificial interrupt
        while True:
            # read lines from serial and parse them
            event_bool = self._read_parse_and_check_for_event()
            # when there is an event store it
            if event_bool:
                self._commit_event_dict(self._event_dict)

    def _read_parse_and_check_for_event(self):
        # read a line and directly store it in the raw data
        line = self.ser.readline()
        line_str = str(line)
        if self._output_file is not '':
            with open(self._output_file, 'a') as f:
                f.write(line_str+"\n")

        # get output data_type
        data_type = line_str.split(':')[0]

        # check if we have the type in our event dict
        if data_type in self._event_dict.keys():
            # do a second sanity check
            if (not (line_str.count(';') == 1)):
                return False
            data = line_str.split(':')[1].split(';')[0]
            try:
                self._event_dict[data_type] = float(data)
            except ValueError as e:
                print("Error while converting a number from the following line: " + str(line_str))
                print(e)
                return False
            # mark the value as recieved
            self._event_dict_confirmed[data_type] = True
            return False

        # check for gps
        if data_type == "PPS":
            gps_lock_sting = line_str.split(':')[2]
            gps_lock_sting = gps_lock_sting.split(';')[0]
            # sanity check
            if (len(gps_lock_sting) == 1):
                self._gps_ok = bool(int(gps_lock_sting))
                # increment the time as well (with that we should be on the safe side of having events at the right time
                self._event_dict['UTCUnixTime'] += 1;

        # check for GPS stings
        gps_type = line_str.split(',')[0]
        # check for a date string
        if gps_type == "$GPZDA":
            # sanity check
            if not (line_str.count(',') == 6):
                return False
            g_time_string = line_str.split(',')[1].split('.')[0]    # has format hhmmss
            hour = int(g_time_string[0:2])
            minute = int(g_time_string[2:4])
            second = int(g_time_string[4:6])
            day = int(line_str.split(',')[2])
            month = int(line_str.split(',')[3])
            year = int(line_str.split(',')[4])
            self._time_from_gps = datetime.datetime(year,
                                                    month,
                                                    day,
                                                    hour,
                                                    minute,
                                                    second,
                                                    tzinfo=None)
            self._event_dict['UTCUnixTime'] = (self._time_from_gps - datetime.datetime(1970,1,1)).total_seconds()
            self._event_dict_confirmed['UTCUnixTime'] = True
            tt = self._event_dict['UTCUnixTime']
            return False

        # check for a location string
        if gps_type == "$GPGGA":
            # sanity check
            if not (line_str.count(',') == 14):
                return False
            # use this as documentation for the string: http://aprs.gids.nl/nmea/#gga
            lat = line_str.split(',')[2]
            lat = float(lat[0:2])
            minutes = line_str.split(',')[2]
            minutes = float(minutes[2:len(minutes)])
            lat += minutes / 60.
            if line_str.split(',')[3] == 'S':
                lat = -lat
            lon = line_str.split(',')[4]
            lon = float(lon[0:3])
            minutes = line_str.split(',')[4]
            minutes = float(minutes[3:len(minutes)])
            lon += minutes / 60.
            if line_str.split(',')[5] == 'W':
                lon = -lon

            self._event_dict['Latitude'] = lat
            self._event_dict_confirmed['Latitude'] = True
            self._event_dict['Longitude'] = lon
            self._event_dict_confirmed['Longitude'] = True
            return False


        # do a pre check if we have all data for a full event stack
        if self._gps_ok == False:
            return False
        if not self._all_data_collected:
            for element in self._event_dict_confirmed:
                if bool(self._event_dict_confirmed[element]) == False:
                    return False
            # if we arrive here we have enough data and the check is obsolete
            self._all_data_collected = True

        # check if we have an event
        if data_type == "Event":
            # sanity check
            if not( (line_str.count(':')==3) and (line_str.count(';')==1) ):
                return False
            sub_sec_string = line_str.split(':')[2]
            sub_sec_string = sub_sec_string.split(';')[0]
            # currently we are getting micros() here
            # so divide them by
            self._event_dict['SubSeconds'] = float(sub_sec_string) / 1000000.0
            # make sure we have a connection to the GPS
            return True
        return False

#det = detector("Test1", "TestVersion1", config_sqlite_location)
#det._commit_event_dict(det._example_event_dict)

det = CosmicPi_V15("COM5", 115200, config_sqlite_location, raw_output_file='1-5_raw_output.log')
#det.start()
print "det init"
while True:
    # read lines from serial and parse them
    print "reading line"
    event_bool = det._read_parse_and_check_for_event()
    # when there is an event store it
    if event_bool:
        print "sending event"
        det._commit_event_dict(det._event_dict)
