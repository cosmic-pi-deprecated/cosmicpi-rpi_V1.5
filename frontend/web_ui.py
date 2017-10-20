from flask import Flask, flash, redirect, render_template, request, make_response
import matplotlib.pyplot as plt
import io
import base64
import c3pyo as c3
import sqlite3
import numpy as np
import matplotlib.dates as mdates

app = Flask(__name__)

sqlite_location = "../storage/sqlite_db"
def initDB():
    conn = sqlite3.connect(sqlite_location)
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
def dashboard():
    values_to_display =[{'name':'Hardware Serial', 'value':getserial(), 'icon':'fa fa-microchip fa-5x'}]
    # get the latest datapoint
    conn = sqlite3.connect(sqlite_location)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events ORDER BY UTCUnixTime DESC, SubSeconds DESC;")
    latest_datapoint = cursor.fetchone()
    # get collumn names
    cursor.execute("PRAGMA table_info(Events);")
    col_names = cursor.fetchall()
    print latest_datapoint
    print col_names

    for i in range(0,len(col_names)):
        # skip the subseconds
        if i == 1:
            continue;
        values_to_display.append({'name':col_names[i][1], 'value':latest_datapoint[i], 'icon':icon_dict[col_names[i][1]]})

    return render_template('dashboard.html', values_to_display=values_to_display)


@app.route('/histogram.png')
def build_plot():
    # get user set parameters
    start_time = request.args.get('start_time', type=int)
    end_time = request.args.get('end_time', type=int)
    bin_size_seconds = request.args.get('bin_size_seconds', type=int)
    plot_title = ''

    # get some data
    data = []
    conn = sqlite3.connect(sqlite_location)
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
    initDB()
    app.run()
