import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, '..', 'bot_db.db')

Base = declarative_base()


class Times(Base):
    __tablename__ = 'times'

    id = Column('id', Integer, primary_key=True)
    recording_date = Column(Integer, nullable=False)
    recording_time = Column(Integer, nullable=False)
    work_time = Column(Integer, nullable=False)
    rest_time = Column(Integer, nullable=False)
    dinner_time = Column(Integer, nullable=False)


engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

time = Times()
time.id = 1
time.recording_date = 2
time.recording_time = 3
time.work_time = 4
time.rest_time = 5
time.dinner_time = 6


session.add(time)
session.commit()
session.close()
