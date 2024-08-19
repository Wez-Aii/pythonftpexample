import logging
from time import sleep
from sqlalchemy import ForeignKey, create_engine, MetaData, Table, Column, Integer, DECIMAL, String, select, Boolean
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session
import os
import psycopg2


POSTGRES_DB_ADDRESS = os.getenv("POSTGRES_DB_ADDRESS", "192.168.1.116")
POSTGRES_DB_PORT = int(os.getenv("POSTGRES_DB_PORT", "54321"))
POSTGRES_DM_USERNAME = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DM_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "dev")


class ConnectionInstance:
    def __init__(self, dialect:str="postgresql", driver:str="psycopg2", username:str=POSTGRES_DM_USERNAME, password:str=POSTGRES_DM_PASSWORD, host_addr:str=POSTGRES_DB_ADDRESS, port:int=POSTGRES_DB_PORT, database_name:str="longansorterclouddb") -> None:
        self.dialect = dialect
        self.driver = driver
        self.host_addr = host_addr
        self.port = port
        self.database_name = database_name
        url = URL.create(
            drivername=f"{self.dialect}+{self.driver}",
            username=username,
            password=password,
            host=self.host_addr,
            port=self.port,
            database=self.database_name
        )
        self.engine = create_engine(url=url)
        self.sessionmaker = sessionmaker(bind=self.engine)
    
    def create_session(self, **kwargs) -> Session:
        return self.sessionmaker(**kwargs)
    
    def close_session(self, session: Session):
        session.close()

    def end_connection(self):
        self.sessionmaker.close_all()



if __name__=="__main__":
    # _instance = ConnectionInstance()
    # _session = _instance.create_session()
    # # Do some process
    # _instance.close_session(_session)
    # _instance.end_connection()
    pass
