from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from docker_data_collector import get_containers_data


class Container_data(Resource):
    def get(self):
        container_data = get_containers_data()
        return container_data

app = Flask(__name__)
api = Api(app)
api.add_resource(Container_data, '/container_data')

if __name__ == '__main__':
    app.run(port='5002')