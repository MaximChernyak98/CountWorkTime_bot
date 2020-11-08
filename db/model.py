import os1
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, '..', 'bot_db.db')

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()


class Times(Base):
    __tablename__ = 'times'

    id = Column(Integer, primary_key=True)
    recording_date = Column(Date, nullable=False)
    recording_time = Column(Time, nullable=False)
    work_time = Column(Time, nullable=False)
    rest_time = Column(Time, nullable=False)
    dinner_time = Column(Time, nullable=False)

    hour = Column(Integer)


Base.metadata.create_all(engine)
