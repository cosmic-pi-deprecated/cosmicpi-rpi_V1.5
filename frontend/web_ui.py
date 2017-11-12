import matplotlib
matplotlib.use('Agg')
from flask import Flask, flash, redirect, render_template, request, make_response
import matplotlib.pyplot as plt
import io
import sqlite3
import matplotlib.dates as mdates
from flask_googlemaps import GoogleMaps
import csv
from flask_basicauth import BasicAuth
import configparser


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
print(UI_USER, UI_PASS)


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
                 (UTCUnixTime INTEGER, SubSeconds REAL, TempreatureC REAL, Humidity REAL, AccelX REAL,
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
            'TempreatureC': "fa fa-thermometer-half fa-5x",
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
    return render_template('settings.html')


@app.route('/CosmicPi_data.csv', methods=['GET'])
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


@app.route('/histogram.png')
def build_plot():
    # get user set parameters
    start_time = request.args.get('start_time', type=int)
    end_time = request.args.get('end_time', type=int)
    bin_size_seconds = request.args.get('bin_size_seconds', type=int)
    plot_title = ''

    # get some data
    data = []
    conn = sqlite3.connect(SQLITE_LOCATION, timeout=60.0)
    cursor = conn.cursor()
    # only get the last n seconds if the start time was negative
    if start_time < 0:
        plot_title += "Histogram of events over the last " + str(-start_time/60) + " minutes\nbin size: "+str(bin_size_seconds)+" [s]"
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
        #event_time_list = [data[i][0] for i in range(len(data))]
        bin_edges = range(int(event_time_list[len(event_time_list) - 1]), int(event_time_list[0]), bin_size_seconds)
        x_axis_limits = (int(event_time_list[len(event_time_list) - 1]), int(event_time_list[0])+1)
        # convert our unix timestamps to Matplotlib  format
        event_time_list = mdates.epoch2num(event_time_list)
        bin_edges = mdates.epoch2num(bin_edges)
        x_axis_limits = mdates.epoch2num(x_axis_limits)

        # make the plot
        plt.hist(event_time_list,bins=bin_edges)
        plt.title(plot_title)
        plt.xlabel("Time [UTC]")
        plt.ylabel("Number of Events [1]")

        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        plt.tick_params(which='both', width=2, direction="out", top=False, right=False)
        plt.tick_params(which='major', length=5)
        plt.tick_params(which='minor', length=3, color='r')

        # do the date formatting
        ax = plt.gca()
        locator = mdates.AutoDateLocator(minticks=7)
        locator.intervald[mdates.SECONDLY] = [1,10,30]
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
    response = make_response(img.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response



if __name__ == '__main__':
    # do necessary inits
    initDB()
    GoogleMaps(app, key="AIzaSyD_RgwMc6X6LpkAmskk4fWmafNFXtlB7_s")
    app.run()
