from datetime import datetime, timedelta
from random import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from cloud_iot.db.models.api import engine, Base, Session
from cloud_iot.db.models.sample import Sample
from cloud_iot.db.models.sensor import Sensor

from cloud_iot.config.config import load_config


Base = declarative_base()
app_config = load_config()
engine = create_engine(app_config['db_connect_str'])
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(bind=engine)

session = Session()

sensor_1 = Sensor()
sensor_1.name = 'Node 1'
session.add(sensor_1)

sensor_2 = Sensor()
sensor_2.name = 'Node 2'
session.add(sensor_2)

current_time = datetime.now()

for i in range(40):
    sample = Sample()
    minutes_delta = 10*i
    time = current_time + timedelta(minutes=minutes_delta)
    value = randint(1, 100)
    sample.sampled_at = time
    sample.value = value
    sensor_1.samples.append(sample)
    session.add(sample)

for i in range(40):
    sample = Sample()
    minutes_delta = 10*i
    time = current_time + timedelta(minutes=minutes_delta)
    value = randint(1, 100)
    sample.sampled_at = time
    sample.value = value
    sensor_2.samples.append(sample)
    session.add(sample)


try:
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()
