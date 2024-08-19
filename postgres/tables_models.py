from typing import Any
from sqlalchemy import ForeignKey, create_engine, MetaData, Table, Column, Integer, DECIMAL, String, select, Boolean, TIMESTAMP, DATE
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase, Mapped


class Base(DeclarativeBase):
    pass

class CRUD():
    def save(self, db_session):
        if self.id == None: # type: ignore
            db_session.add(self)
                
        return db_session.commit()

    def destroy(self, db_session):
        db_session.delete(self)
        return db_session.commit()
    
    def get_id(self, db_session):
        db_session.refresh(self)
        return self.id # type: ignore
    

class OtuLoginDm(Base, CRUD):
    __tablename__ = "otu_login_dm"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    is_active = Column(Boolean)
    # created_at = Column(TIMESTAMP)
    timestamp = Column(TIMESTAMP)

    def __init__(self, username, password, is_active, timestamp, id=None):
        self.username = username
        self.password = password
        self.is_active = is_active
        self.timestamp = timestamp
        self.id = id