# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.24.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from flask_restful import Resource


class Sample(Resource):

    def get(self, id):
        return 'sample get'

    def put(self, id):
        pass

    def post(self, id):
        pass

    def delete(self, id):
        pass

    def update(self, id):
        pass


class SampleList(Resource):

    def get(self):
        return 'sample get'
