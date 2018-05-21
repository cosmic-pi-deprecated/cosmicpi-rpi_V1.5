from flask import request
from flask_restful import Resource
from cosmicpi.config import Config
from .auth import requires_auth
import subprocess
import re
import time
import os
from functools import wraps
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
        psk = request.form['pass']

        # Try to connect to a new Wifi
        wpa_supplicant_content = """
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="%s"
    psk="%s"
    id_str="AP1"
}
    """ % (ssid, psk)
        with open(WPA_SUPPLICANT_LOCATION, 'w') as file:
            file.write(wpa_supplicant_content)
        os.system('sudo ifdown --force wlan0; sudo ifup wlan0')

        # Get new IP
        new_ip = subprocess.check_output(
            "ifconfig wlan0 | awk '/inet / {print $2}'", 
            shell=True
            ).decode('utf-8').strip()

        # Return result
        if len(new_ip) > 0:
            return {
                'message': 'Great! Your are not connected to %s and you can access to ' \
                'this web panel on http://%s/' % (ssid, new_ip),
            }
        return { 'message': 'Something went wrong, unable to connect :(' }