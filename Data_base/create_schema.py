import urllib.parse
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Boolean, Table, PrimaryKeyConstraint, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from Data_base.password import password


Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    sex = Column(Integer, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    bdate = Column(Date)
    year_birth = Column(Integer)
    ses = relationship('Ses', cascade="all,delete", backref='client')
    entry = relationship('Entry', cascade="all,delete", backref='client')


class Ses(Base):
    __tablename__ = 'ses'

    session_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    time_session = Column(Time)
    message = relationship('Message', cascade="all,delete", backref='ses')


class Message(Base):
    __tablename__ = 'message'

    message_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("ses.session_id"), nullable=False)
    time_message = Column(Time)
    message = Column(Text)


class Entry(Base):
    __tablename__ = 'entry'

    entry_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    service_id = Column(Integer, ForeignKey("service.service_id"), nullable=False)
    time_entry = Column(Time)


class Service(Base):
    __tablename__ = 'service'

    service_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Integer)
    entry = relationship('Entry', cascade="all,delete", backref='service')


def create_schema():
    pswrd = urllib.parse.quote_plus(password)
    db = f"mysql+mysqlconnector://rs1180w5_vk_oks:{pswrd}@rs1180w5.beget.tech:3306/rs1180w5_vk_oks"
    engine = create_engine(db, echo=True)
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_schema()
