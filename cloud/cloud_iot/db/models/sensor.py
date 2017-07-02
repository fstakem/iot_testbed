# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.24.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, Numeric
from sqlalchemy.orm import relationship

from cloud_iot.db.models.api import Base
from cloud_iot.db.models.base_model import BaseModel


class Sensor(BaseModel, Base):

    # Properties
    sensor_id               = Column(Integer, primary_key=True)
    name                    = Column(String(100), nullable=False)
    
    # Constraints

    # Relationships
    samples                 = relationship("Sample", backref="sensor")

    __tablename__ = 'sensor'
