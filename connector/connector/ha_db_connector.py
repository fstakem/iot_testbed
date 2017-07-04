# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    7.3.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
import requests
import time
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from homeassistant.components.recorder.models import States


db_str = 'sqlite:////home/homeassistant/.homeassistant/home-assistant_v2.db'
sensor_ids = [ 'sensor.yr_symbol' ]

Base = declarative_base()
engine = create_engine(db_str)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(bind=engine)

session = Session()

while True:
    for sensor_id in sensor_ids:
        states = session.query(States).filter(States.entity_id==sensor_id)

        for state in states:
            output = '%s %s %s' % (state.last_updated, state.state, state.attributes)

            url = "http://localhost:5000/samples"

            # Fill in data from states
            data = {
                "sensor_id": "1",
                "sampled_at": "2017-05-20 04:05:25",
                "value": "45"
            }
            response = requests.post(url, json=data)

            print(response.status_code)
            print(response.text)


    sleep_time_sec = 60 * 5
    time.sleep(sleep_time_sec)


#2017-07-04 00:06:26.232546 1 {"entity_picture": "//api.met.no/weatherapi/weathericon/1.1/?symbol=1;content_type=image/png", "friendly_name": "yr Symbol",
# "attribution": "Weather forecast from yr.no, delivered by the Norwegian Meteorological Institute and the NRK."}

# state_id = Column(Integer, primary_key=True)
# domain = Column(String(64))
# entity_id = Column(String(255))
# state = Column(String(255))
# attributes = Column(Text)
# event_id = Column(Integer, ForeignKey('events.event_id'))
# last_changed = Column(DateTime(timezone=True), default=datetime.utcnow)
# last_updated = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
# created = Column(DateTime(timezone=True), default=datetime.utcnow)
