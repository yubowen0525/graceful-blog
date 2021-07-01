from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from src.extension import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_time = Column(DateTime, nullable=False, default=datetime.utcnow)