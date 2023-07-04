from fastapi import HTTPException, status

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from configparser import ConfigParser


config = ConfigParser()
config.read("src/conf/config.ini")

user = config.get('DB', 'user')
password = config.get('DB', 'password')
host = config.get('DB', 'host')
port = config.get('DB', 'port')
db_name = config.get('DB', 'db_name')

url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(url)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = Session()

    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()