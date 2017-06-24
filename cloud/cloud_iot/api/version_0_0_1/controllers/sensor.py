# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.24.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from flask_restful import Resource


class Sensor(Resource):

    def get(self, id):
        return 'sensor get'

    def put(self, id):
        pass

    def post(self, id):
        pass

    def delete(self, id):
        pass

    def update(self, id):
        pass


class SensorList(Resource):

    def get(self):
        return 'sensors get'
