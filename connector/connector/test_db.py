from datetime import datetime

from sqlalchemy import create_engine, and_
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
last_filter_time = datetime.now()

for sensor_id in sensor_ids:
    states = session.query(States).filter(and_(States.entity_id==sensor_id, States.last_updated > last_filter_time))

    for state in states:
        output = '%s %s %s' % (state.last_updated, state.state, state.attributes)