import matplotlib
matplotlib.use('Agg')
from flask import request, make_response
from flask_restful import Resource
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import sqlite3
from cosmicpi.config import Config


SQLITE_LOCATION = Config.get("Storage", "sqlite_location")


class Histogram(Resource):
    def get(self):
        start_time = int(request.args['from'])
        end_time = int(request.args['to'])
        bin_size_seconds = int(request.args['bin_size'])

        # render the plot
        img = build_histogram(start_time, end_time, bin_size_seconds)

        # return the plot
        response = make_response(img)
        response.headers['Content-Type'] = 'image/png'

        return response


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

