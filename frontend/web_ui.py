from flask import Flask, flash, redirect, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import c3pyo as c3

app = Flask(__name__)


@app.route("/base/")
def base():
    return render_template(
        'cosmic_base.html', **locals())

def get_line_chart_json():
    # data
    x = [1, 2, 3, 4, 5, 6, 7]
    y1 = [150, 450, 200, 100, 300, 0, 325]
    y2 = [230, 220, 150, 400, 105, 50, 302]

    # chart
    chart = c3.LineChart()
    chart.plot(x, y1, label='Series 1')
    chart.plot(x, y2, label='Series 2')
    chart.bind_to('line_chart_div')
    return chart.json()

@app.route('/test/', methods=['GET', 'POST'])
def test():
    chart_json = get_line_chart_json()
    return render_template('c3pyo.html', chart_json=chart_json)

@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    chart_json = get_line_chart_json()
    return render_template('dashboard.html', chart_json=chart_json)

@app.route('/plot/')
def build_plot():

    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


if __name__ == '__main__':
    app.run()
