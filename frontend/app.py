from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from .params import Params
from .wifi import Wifi
from .histogram import Histogram
from .data import Data

app = Flask(__name__)
api = Api(app)

CORS(app, resources=r'/api/*')

api.add_resource(Params, '/api/params')
api.add_resource(Wifi, '/api/wifi')
api.add_resource(Histogram, '/api/histogram.png')
api.add_resource(Data, '/api/data')

if __name__ == '__main__':
    app.run(debug=True)
