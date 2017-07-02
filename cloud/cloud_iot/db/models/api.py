# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.16.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from cloud_iot.config.config import load_config


Base = declarative_base()
app_config = load_config()
engine = create_engine(app_config['db_connect_str'])
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    

    