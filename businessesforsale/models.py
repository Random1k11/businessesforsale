# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
import datetime


Base = declarative_base()

def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)

engine = db_connect()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()



class Businesses(Base):

    __tablename__ = 'businesses'

    id           = Column(Integer, primary_key=True)
    title        = Column(String(500))
    location     = Column(String(300))
    asking_price = Column(String(300))
    sales_revenu = Column(String(300))
    cash_flow    = Column(String(300))
    currency     = Column(Text)
    description  = Column(Text)
    details      = Column(Text)
    listing_id   = Column(String(300), unique=True)
    URL          = Column(Text)
    created_date = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Title: {}, URL: {}>'.format(self.title, self.URL)


def check_existence_row_in_db(listing_id):
    return session.query(Businesses).filter(Businesses.listing_id == listing_id).first()


def get_value_from_databse(listing_id):
    return session.query(Businesses).filter(Businesses.listing_id == listing_id).first()


def update_values(listing_id, result):
    session.query(Businesses).filter(Businesses.listing_id == listing_id).update(dict(title=result[0], location=result[1],
                                                                                      asking_price=result[2], sales_revenu=result[3],
                                                                                      cash_flow=result[4], currency=result[5],
                                                                                      description=result[6], URL=result[7], 
                                                                                      created_date=datetime.datetime.now()))
    session.commit()
