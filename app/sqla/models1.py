from sqlalchemy import Column, Integer, String
from app.db import Base  # Assuming you have a Base class for SQLAlchemy models
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Observation(db.Model):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String)
    site = Column(String)
    greenhouse = Column(String)
    cycle_name = Column(String)
    copy = Column(Integer)
