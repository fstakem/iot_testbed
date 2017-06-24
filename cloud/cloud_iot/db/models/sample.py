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


class Sample(BaseModel):

    # Properties
    sample_id               = db.Column(db.Integer, primary_key=True)
    sampled_at              = db.Column(db.DateTime)
    value                   = db.Column(db.String(1000), nullable=False)
    
    # Constraints
    sensor_id               = db.Column(db.Integer, db.ForeignKey('sensor.sensor_id'))

    # Relationships

    __tablename__ = 'sample'
