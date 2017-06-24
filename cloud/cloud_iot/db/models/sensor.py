# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.24.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from cloud_iot.db.models.base_model import BaseModel
from cloud_iot.database import acl_db as db


class Sensor(BaseModel):

    # Properties
    sensor_id               = db.Column(db.Integer, primary_key=True)
    name                    = db.Column(db.String(100), nullable=False)
    
    # Constraints

    # Relationships
    samples                 = db.relationship("Sample", backref="sensor")

    __tablename__ = 'sensor'
