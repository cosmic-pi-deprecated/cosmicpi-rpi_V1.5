from flask import Flask, request
from flask_restful import Api
from .params import Params
from .wifi import Wifi

app = Flask(__name__)
api = Api(app)

api.add_resource(Params, '/params')
api.add_resource(Wifi, '/wifi')

if __name__ == '__main__':
    app.run(debug=True)
