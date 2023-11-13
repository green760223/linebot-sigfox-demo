import datetime

from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String(50), primary_key=True)
    device_id = Column(String(50), nullable=False)
    created_time = Column(DateTime(), nullable=False)

    def __init__(self, id, device_id):
        self.id = id
        self.created_time = datetime.datetime.now()
        self.device_id = device_id

    def __repr__(self):
        return '<User %r>' % (self.id)
