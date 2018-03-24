from flask import request
from flask_restful import Resource
from cosmicpi.config import Config
from .auth import requires_auth
import subprocess
import re
import time
from functools import wraps
try:
    import thread
except:
    import _thread as thread
try:
    import urllib2
except:
    import urllib3 as urllib2


DEFAULT_WIFI_NAME = Config.get("Default WiFi", "name")
DEFAULT_WIFI_PASS = Config.get("Default WiFi", "password")
WPA_SUPPLICANT_LOCATION = Config.get("MISC", "wpa_supplicant_location")


class Wifi(Resource):
    @requires_auth
    def get(self):
        # Get current network
        connected_network_name_response = ''
        try:
            connected_network_name_response = subprocess.check_output(['sudo', 'iwgetid'])
        except subprocess.CalledProcessError as e:
            err_text = 'ERROR get connected network: %s' % str(e)
            connected_network_name_response = err_text
            print(err_text)
        connected_network_name_str = re.findall('\"(.*?)\"', connected_network_name_response)

        if len(connected_network_name_str) < 1:
            connected_network_name_str = ''
        else:
            connected_network_name_str = connected_network_name_str[0]

        # Available networks
        wifi_network_list = [connected_network_name_str]
        available_networks_response = ''
        try:
            available_networks_response = subprocess.check_output(['sudo', 'iw', 'dev', 'wlan0', 'scan'])
        except subprocess.CalledProcessError as e:
            err_text = 'ERROR get list of networks: %s' % str(e)
            print(err_text)
            available_networks_response = err_text
        available_networks_lines = available_networks_response.split('\n')
        for availableNetworksLine in available_networks_lines:
            if 'SSID' in availableNetworksLine:
                essid = availableNetworksLine.replace('SSID:', '').strip()
                wifi_network_list.append(essid)
        wifi_network_list = filter(lambda x: x != '', wifi_network_list)

        # Print everything
        return {
            'current': connected_network_name_str,
            'available': wifi_network_list,
        }

    @requires_auth
    def post(self):
        ssid = request.form['ssid']
        password = request.form['pass']

        thread.start_new_thread(connect_to_wifi, (ssid, password))

        msg = 'The CosmicPi will now try to connect to the WiFi "{}". ' \
              "If no internet connection is found or the connection was not " \
              "successful the CosmiPi will recreate the WiFi hotspot. Please " \
              "wait at least two minutes.".format(ssid)
        return {
            'message': msg
        }


def fall_back_to_ap():
    # empty the wpa supplicant to it's default
    wpa_supplicant_string = "country=GB\n"  # Todo: Check, that this string in front is still correct!
    wpa_supplicant_string += "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n"
    wpa_supplicant_string += "update_config=1\n"
    wpa_supplicant_string += "\nnetwork={\n"
    net = (DEFAULT_WIFI_NAME, DEFAULT_WIFI_PASS)
    wpa_supplicant_string += '\tssid="{}"\n'.format(net[0])
    # check if we need a password
    if str(net[1]) == "":
        wpa_supplicant_string += '\tpsk="{}"\n'.format(net[1])
    wpa_supplicant_string += "}\n"
    with open(WPA_SUPPLICANT_LOCATION, 'w') as file:
        file.write(wpa_supplicant_string)
    # configure controler to accept the new configuration
    try:
        import fcntl
        time.sleep(2)
        subprocess.call("wpa_cli -i wlan0 reconfigure", shell=True)
        time.sleep(2)
    except ImportError:
        print("This OS is not linux enough to handle a hotspot in this way")

    # restart the hotspot
    try:
        import fcntl
        subprocess.call("systemctl start dnsmasq",
                        shell=True)  # well, here we actually care if the hotspot starts, but oh well...
        time.sleep(2)
        subprocess.call("ifconfig wlan0 down", shell=True)
        time.sleep(2)
        subprocess.call("ifconfig wlan0 up", shell=True)
    except ImportError:
        print("This OS is not linux enough to handle a hotspot in this way")


def connect_to_wifi(name, pw):
    # build the string for the WPA supplicant
    wpa_supplicant_string = "country=GB\n"    # Todo: Check, that this string in front is still correct!
    wpa_supplicant_string += "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n"
    wpa_supplicant_string += "update_config=1\n"
    networks = [(name, pw), (DEFAULT_WIFI_NAME, DEFAULT_WIFI_PASS)]
    for net in networks:
        wpa_supplicant_string += "\nnetwork={\n"
        wpa_supplicant_string += '\tssid="{}"\n'.format(net[0])
        # check if we need a password
        if not str(net[1]) == "":
            wpa_supplicant_string += '\tpsk="{}"\n'.format(net[1])
        wpa_supplicant_string += "}\n"

    # deactivate htospot and turn the WiFi back on
    try:
        import fcntl
        subprocess.call("systemctl stop dnsmasq", shell=True)  # we very much don't care if this fails
        time.sleep(2)
        subprocess.call("ifconfig wlan0 down", shell=True)
        time.sleep(2)
        subprocess.call("ifconfig wlan0 up", shell=True)
    except ImportError:
        print("This OS is not linux enough to handle a hotspot in this way")
    # write wpa_supplicant string to the file
    with open(WPA_SUPPLICANT_LOCATION, 'w') as file:
        file.write(wpa_supplicant_string)
    # configure controler to accept the new configuration
    try:
        import fcntl
        time.sleep(2)
        subprocess.call("wpa_cli -i wlan0 reconfigure", shell=True)
    except ImportError:
        print("This OS is not linux enough to handle a hotspot in this way")

    # wait for an internet connection (max 2 min)
    start_time = time.time()
    have_internet = False
    while not have_internet and ((start_time + 120) > time.time()):
        have_internet = internet_on()

    # if we have no internet, restart the hotspot, otherwise we are done for now
    if have_internet:
        print("Successfully connected to the internet (yeah)")
        # wait a bit before we send the mail
        time.sleep(5)
        # ToDo: This would be a good point to send a mail or something similar to the user.
        # Just to inform them where their cosmicPi is and what's it doing
        return
    else:
        print("No internet connection here, falling back to hotspot!")
        fall_back_to_ap()
        return


def internet_on():
    try:
        urllib2.urlopen('http://heise.de', timeout=2)
        return True
    except urllib2.URLError:
        return False
