# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.24.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, Numeric, ForeignKey

from cloud_iot.db.models.api import Base
from cloud_iot.db.models.base_model import BaseModel


class Sample(BaseModel, Base):

    # Properties
    sample_id               = Column(Integer, primary_key=True)
    sampled_at              = Column(DateTime)
    value                   = Column(String(1000), nullable=False)
    
    # Constraints
    sensor_id               = Column(Integer, ForeignKey('sensor.sensor_id'))

    # Relationships

    __tablename__ = 'sample'
