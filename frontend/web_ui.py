import matplotlib
matplotlib.use('Agg')
from flask import Flask, flash, redirect, render_template, request, make_response
import matplotlib.pyplot as plt
import io
import sqlite3
import matplotlib.dates as mdates
import csv
from flask_basicauth import BasicAuth
import configparser
import subprocess
import urllib2
import time
import thread
import re
import socket
import struct



# read settings
CONFIG_FILE = "../config/CosmicPi.config"
# read configuration
# Todo: Put the config parser into a propper class
# Todo: Implement proper error catching for configparser (e.g. non existent keys or file)
# read configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
SQLITE_LOCATION = config.get("Storage", "sqlite_location")
UI_USER = config.get("UI", "username")
UI_PASS = config.get("UI", "password")
DEFAULT_WIFI_NAME = config.get("Default WiFi", "name")
DEFAULT_WIFI_PASS = config.get("Default WiFi", "password")
WPA_SUPPLICANT_LOCATION = str(config.get("MISC", "wpa_supplicant_location"))

# start flask
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = UI_USER
app.config['BASIC_AUTH_PASSWORD'] = UI_PASS

basic_auth = BasicAuth(app)


def initDB():
    conn = sqlite3.connect(SQLITE_LOCATION, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Events'")
    if cursor.fetchone() == None:
        cursor.execute('''CREATE TABLE Events
                 (UTCUnixTime INTEGER, SubSeconds REAL, TemperatureC REAL, Humidity REAL, AccelX REAL,
                  AccelY REAL, AccelZ REAL, MagX REAL, MagY REAL, MagZ REAL, Pressure REAL, Longitude REAL,
                  Latitude REAL, DetectorName TEXT, DetectorVersion TEXT);''')
        conn.commit()

@app.route("/base/")
def base():
    return render_template(
        'cosmic_base.html', **locals())


@app.route("/hw_serial.txt")
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



icon_dict = {
            'UTCUnixTime': "fa fa-clock-o fa-5x",
            'TemperatureC': "fa fa-thermometer-half fa-5x",
            'Humidity': "fa fa-tint fa-5x",
            'AccelX': "fa fa-tachometer fa-5x",
            'AccelY': "fa fa-tachometer fa-5x",
            'AccelZ': "fa fa-tachometer fa-5x",
            'MagX': "fa fa-compass fa-5x",
            'MagY': "fa fa-compass fa-5x",
            'MagZ': "fa fa-compass fa-5x",
            'Pressure': "fa fa-thermometer-half fa-5x",
            'Longitude': "fa fa-map-marker fa-5x",
            'Latitude': "fa fa-map-marker fa-5x",
            'DetectorName': "fa fa-info-circle fa-5x",
            'DetectorVersion': "fa fa-info-circle fa-5x",
}

@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard_page():
    values_to_display =[{'name':'Hardware Serial', 'value':getserial(), 'icon':'fa fa-microchip fa-5x'}]

    # get the latest datapoint
    conn = sqlite3.connect(SQLITE_LOCATION, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events ORDER BY UTCUnixTime DESC, SubSeconds DESC;")
    latest_datapoint = cursor.fetchone()
    # get collumn names
    cursor.execute("PRAGMA table_info(Events);")
    col_names = cursor.fetchall()
    conn.close()

    # extract data
    for i in range(0,len(col_names)):
        # skip the subseconds
        if i == 1:
            continue;
        # field name
        f_name = col_names[i][1]
        # fill in values
        if f_name in icon_dict.keys():
            values_to_display.append({'name':f_name, 'value':latest_datapoint[i], 'icon':icon_dict[f_name]})

    return render_template('dashboard.html', values_to_display=values_to_display)


@app.route('/plotting/', methods=['GET', 'POST'])
def plotting_page():
    location_vars = {'Latitude': 0, 'Longitude': 0}

    # get the latest datapoint
    conn = sqlite3.connect(SQLITE_LOCATION, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events ORDER BY UTCUnixTime DESC, SubSeconds DESC;")
    latest_datapoint = cursor.fetchone()
    # get collumn names
    cursor.execute("PRAGMA table_info(Events);")
    col_names = cursor.fetchall()
    conn.close()

    # extract data
    for i in range(0,len(col_names)):
        # skip the subseconds
        if i == 1:
            continue;
        # field name
        f_name = col_names[i][1]
        # fill in location
        if f_name in location_vars.keys():
            location_vars[f_name] = latest_datapoint[i]



    return render_template('plotting.html', location_vars=location_vars)

@app.route('/settings/', methods=['GET', 'POST'])
@basic_auth.required
def settings_page():
    current_WiFi, avail_WiFi = get_current_and_available_networks()
    return render_template('settings.html', available_wifis=avail_WiFi, current_wifi=current_WiFi)

def get_current_and_available_networks():
    wifiNetworkList = ''
    # Presently connected network
    connectedNetworkNameResponse = ''
    try:
        connectedNetworkNameResponse = subprocess.check_output(['sudo','iwgetid'])
    except subprocess.CalledProcessError as e:
        print('ERROR get connected network: ')
        print(e)
    except WindowsError as e:
        print("Well, windows just can't do this...")
        connectedNetworkNameResponse = '"No networks found, because the WebUI is beeing executed on windows."'
    connectedNetworkNameStr = re.findall('\"(.*?)\"', connectedNetworkNameResponse) #" Find the string between quotes
    if len(connectedNetworkNameStr) < 1:
        connectedNetworkNameStr = ''
    else:
        connectedNetworkNameStr =connectedNetworkNameStr[0]
    wifiNetworkList = [connectedNetworkNameStr]
    # Available networks
    availableNetworksResponse = ''
    try:
        availableNetworksResponse = subprocess.check_output(['sudo','iw','dev','wlan0','scan'])
    except subprocess.CalledProcessError as e:
        print('ERROR get list of networks: ')
        print(e)
    except WindowsError as e:
        print("Well, windows just can't do this either...")
        availableNetworksResponse = 'SSID: Network A\nSSID: Network B\n'
    availableNetworksLines = availableNetworksResponse.split('\n')
    for availableNetworksLine in availableNetworksLines:
        if 'SSID' in availableNetworksLine:
            # Typical line:
            #   SSID: elithion belkin
            essid = availableNetworksLine.replace('SSID:','').strip()
            wifiNetworkList.append(essid)
    return connectedNetworkNameStr, wifiNetworkList

@app.route('/connect_to_wifi', methods=['GET', 'POST'])
@basic_auth.required
def wifi_connector():
    # get user set parameters
    wifi_name = request.args.get('selected_wifi')
    wifi_pw = request.args.get('password')

    # launch the wifi login in a different thread
    # we need to to it like this, since otherwise the user would never recieve an answer...
    thread.start_new_thread(connect_to_wifi, (wifi_name, wifi_pw))

    msg = 'The CosmicPi will now try to connect to the WiFi "{}". '.format(wifi_name)
    msg += "If no internet connection is found or the connection was not sucessfull the CosmiPi will recreate the WiFi hotspot. Please wait at least two minutes."
    return msg


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        import fcntl
        result = socket.inet_ntoa(fcntl.ioctl(
                                                s.fileno(),
                                                0x8915,  # SIOCGIFADDR
                                                struct.pack('256s', ifname[:15])
                                            )[20:24])
    except IOError:
        print("Error getting the IP address, either you are not doing this on raspbian or the queried device does not exist.")
        result = "no IP on {}".format(ifname)
    except WindowsError:
        print("Getting the IP address on Windows is not implemented")
        result = "no IP on {}".format(ifname)
    except ImportError:
        print("Getting the IP address on this OS is not implemented")
        result = "no IP on {}".format(ifname)
    return  result


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
    while (have_internet == False) and ((start_time + 120) >  time.time()):
        have_internet = internet_on()

    # if we have no internet, restart the hotspot, otherwise we are done for now
    if have_internet:
        print("Sucessfully connected to the internet (yeah)")
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
    except urllib2.URLError as err:
        return False

@app.route('/CosmicPi_data.csv', methods=['GET'])
@basic_auth.required
def csv_export():
    conn = sqlite3.connect(SQLITE_LOCATION, timeout=60.0)
    cursor = conn.cursor()

    # get collumn names
    cursor.execute("PRAGMA table_info(Events);")
    col_data = cursor.fetchall()
    col_names = []
    for i in range(0, len(col_data)):
        col_names.append(col_data[i][1])

    # get data from db
    cursor.execute("SELECT * FROM Events ORDER BY UTCUnixTime DESC, SubSeconds DESC;")
    data = cursor.fetchall()
    conn.close()

    # write CSV export to memory
    output = io.BytesIO()
    writer = csv.writer(output)
    writer.writerow(col_names)
    writer.writerows(data)

    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    return response


@app.route('/about/', methods=['GET', 'POST'])
def about_page():
    return render_template('about.html')


# returns the histogram as a png byte stream
def build_histogram(start_time, end_time, bin_size_seconds):
    plot_title = ''

    # get some data
    data = []
    conn = sqlite3.connect(SQLITE_LOCATION, timeout=60.0)
    cursor = conn.cursor()
    # only get the last n seconds if the start time was negative
    if start_time < 0:
        plot_title += "Histogram of events over the last {0:.1f} minutes\nbin size: {1:d} [s]".format(-start_time / 60.,
                                                                                                      bin_size_seconds)
        cursor.execute("SELECT * FROM Events ORDER BY UTCUnixTime DESC, SubSeconds DESC;")
        start_time = cursor.fetchone()[0] + start_time
        end_time = 9000000000
    else:
        plot_title += "Histogram of events over a set time\nbin size: " + str(bin_size_seconds) + " [s]"
    cursor.execute("SELECT * FROM Events WHERE UTCUnixTime BETWEEN ? AND ? ORDER BY UTCUnixTime DESC, SubSeconds DESC;",
                   (start_time, end_time))
    data = cursor.fetchall()
    conn.close()

    # massage data
    if len(data) == 0:
        plt.hist([])
        plt.title("No data to display")
    else:
        event_time_list = [data[i][0] + data[i][1] for i in range(len(data))]
        # event_time_list = [data[i][0] for i in range(len(data))]
        bin_edges = range(int(event_time_list[len(event_time_list) - 1]), int(event_time_list[0]), bin_size_seconds)
        x_axis_limits = (start_time, int(event_time_list[0]) + 1)
        # convert our unix timestamps to Matplotlib  format
        event_time_list = mdates.epoch2num(event_time_list)
        bin_edges = mdates.epoch2num(bin_edges)
        x_axis_limits = mdates.epoch2num(x_axis_limits)

        # make the plot
        plt.hist(event_time_list, bins=bin_edges)
        plt.title(plot_title)
        plt.xlabel("Time [UTC]")
        plt.ylabel("Number of Events per {0:d} seconds [1]".format(bin_size_seconds))

        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        plt.tick_params(which='both', width=2, direction="out", top=False, right=False)
        plt.tick_params(which='major', length=5)
        plt.tick_params(which='minor', length=3, color='r')

        # do the date formatting
        ax = plt.gca()
        locator = mdates.AutoDateLocator(minticks=7)
        locator.intervald[mdates.SECONDLY] = [1, 10, 30]
        formatter = mdates.AutoDateFormatter(locator)
        formatter.scaled[1 / (24. * 60.)] = '%H:%M:%S'
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.set_xlim(x_axis_limits)

    # return the generated plot
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img.getvalue()

@app.route('/histogram.png')
def serve_histogram_request():
    # get user set parameters
    start_time = request.args.get('start_time', type=int)
    end_time = request.args.get('end_time', type=int)
    bin_size_seconds = request.args.get('bin_size_seconds', type=int)

    # render the plot
    img = build_histogram(start_time, end_time, bin_size_seconds)

    # return the plot
    response = make_response(img)
    response.headers['Content-Type'] = 'image/png'
    return response

def periodically_render_dashboard_histogram():
    while True:
        # standard values for the dashboard histogram
        start_time = -120
        end_time = 9000000000
        bin_size_seconds = 2
        # place where we need to save the image
        path_to_static_image = "static/images/dashboard_histogram.png"

        # render the plot
        img = build_histogram(start_time, end_time, bin_size_seconds)

        # save the image to disk
        with open(path_to_static_image, 'wb') as f:
            f.write(img)

        # wait four seconds until we render the next plot
        time.sleep(4)

if __name__ == '__main__':
    # do necessary inits
    initDB()
    # Launch the periodical histogram renderer for the dashboard
    thread.start_new_thread(periodically_render_dashboard_histogram, ())
    app.run()
