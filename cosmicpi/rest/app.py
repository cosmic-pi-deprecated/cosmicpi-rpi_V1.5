from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from .wifi import Wifi
from .histogram import Histogram
from .series import Series
from .auth import Auth

def create_app():
    app = Flask(__name__)
    api = Api(app)

    CORS(app, resources=r'/api/*')

    api.add_resource(Auth, '/api/auth')
    api.add_resource(Wifi, '/api/wifi')
    api.add_resource(Histogram, '/api/histogram.png')
    api.add_resource(Series, '/api/series')
    
    return app

if __name__ == '__main__':
    create_app().run(debug=True)
