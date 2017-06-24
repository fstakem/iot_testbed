# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.24.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from flask import Blueprint, render_template, abort, request, redirect, session
from flask import current_app
from flask_restful import Api, Resource, url_for
from jinja2 import TemplateNotFound

from cloud_iot.api.version_0_0_1.controllers.sensor import Sensor as SensorController
from cloud_iot.api.version_0_0_1.controllers.sensor import SensorList as SensorListController
from cloud_iot.api.version_0_0_1.controllers.sample import Sample as SampleController
from cloud_iot.api.version_0_0_1.controllers.sample import SampleList as SampleListController

#from cloud_iot.db.models.person import Person
from cloud_iot.database import acl_db as db


version_value = '0_0_1'
version_name = 'app_v' + version_value

app_v0_0_1 = Blueprint(version_name, version_name, 
    static_folder='cloud_iot/api/version_0_0_1/static', 
    static_url_path='',
    template_folder='cloud_iot/api/version_0_0_1/templates')


# Web routes
@app_v0_0_1.route('/')
def version_hello():
    return 'v0.0.1'

@app_v0_0_1.route('/index')
def index():
    return render_template('index.html')


# Basic restful routes
rest_api = Api(app_v0_0_1)

rest_api.add_resource(SensorController, '/sensor/<int:id>')
rest_api.add_resource(SensorListController, '/sensor/all')
rest_api.add_resource(SampleController, '/sample/<int:id>')
rest_api.add_resource(SampleListController, '/sample/all')




