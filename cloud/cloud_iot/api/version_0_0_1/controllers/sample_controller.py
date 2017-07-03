# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.24.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from flask import jsonify
from flask_restful import Resource, reqparse, abort, Api

from cloud_iot.db.models.sensor import Sensor
from cloud_iot.db.models.sample import Sample


class SampleController(Resource):

    def get(self, id):
        return 'sample get'

    def put(self, id):
        pass

    def delete(self, id):
        pass

    def update(self, id):
        pass


class SampleListController(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('sensor_id', type=int)
    parser.add_argument('sampled_at', type=str)
    parser.add_argument('value', type=str)

    def get(self):
        return 'sample get'

    def post(self):
        args = SampleListController.parser.parse_args()
        sensor_id = int(args['sensor_id'])
        sampled_at = str(args['sampled_at'])
        value = str(args['value'])

        return jsonify(id=sensor_id, sampled_at=sampled_at, value=value)
