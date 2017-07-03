# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.24.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from flask import jsonify
from datetime import datetime
from flask_restful import Resource, reqparse, abort, Api

from cloud_iot.db.models.api import Session
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
        sampled_at = None
        value = None

        session = Session()
        sensor = session.query(Sensor).get(sensor_id)

        if sensor:
            sampled_at_str = str(args['sampled_at'])
            try:
                sampled_at = datetime.strptime(sampled_at_str, "%Y-%m-%d %H:%M:%S")
                value = str(args['value'])

                sample = Sample()
                sample.sampled_at = sampled_at
                sample.value = value
                sensor.samples.append(sample)
                session.add(sensor)
                session.add(sample)
                session.commit()
            except ValueError as err:
                pass

        return jsonify(id=sensor_id, sampled_at=sampled_at, value=value)
