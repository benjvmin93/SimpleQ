from sqlalchemy import Column, Integer,JSON, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Circuit(Base):
    __tablename__ = "circuits"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    circuit = Column(JSON)
    # username = Column(String, unique=True, index=True)
    # email = Column(String, unique=True, index=True)
    # user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship('User')


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
