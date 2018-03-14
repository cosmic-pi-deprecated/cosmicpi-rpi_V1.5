from flask import Flask, request
from flask_restful import Api
from .params import Params
from .wifi import Wifi
from .histogram import Histogram
from .data import Data

app = Flask(__name__)
api = Api(app)

api.add_resource(Params, '/params')
api.add_resource(Wifi, '/wifi')
api.add_resource(Histogram, '/histogram.png')
api.add_resource(Data, '/data')

if __name__ == '__main__':
    app.run(debug=True)
