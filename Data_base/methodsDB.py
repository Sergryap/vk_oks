import urllib.parse
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from Data_base.password import password
from Data_base.create_schema import Client, Entry, Service, Message


class DbMethods:
    """
    Класс методов взаимодействия с базой данных,
    не вошедших в декоратор db_connect
    """

    pswrd = urllib.parse.quote_plus(password)
    db = f"mysql+mysqlconnector://rs1180w5_vk_oks:{pswrd}@rs1180w5.beget.tech:3306/rs1180w5_vk_oks"
    engine = create_engine(db, echo=False)
    conn = engine.connect()
    Session = sessionmaker(bind=engine)