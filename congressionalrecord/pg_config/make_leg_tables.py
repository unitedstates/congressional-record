import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def make_psql_engine(user,db):
    """
    Just a helper, but you could use it
    to build a Postgres+Psycopg2 connector
    i.e., engine = make_psql_engine(user,db)
    """
    engine_str = "postgresql+psycopg2://{0}@/{1}".format(user,db)
    engine = create_engine(engine_str)
    return engine

def build_all_tables(session,user,db):
    """
    Build all the tables bound to Base
    Give it a session first, it lives
    outside the function for
    subsequent use if desired
    i.e. session = sessionmaker()
    """
    engine = make_psql_engine(user,db)
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

class LegBio(Base):
    """
    Defines table name and columns for one of several tables
    constructed from an entry in legislators-current.yaml
    or legislators-historical.yaml
    """
    __tablename__ = 'leg_bio'
    bioguideid = Column(String(7), primary_key=True)
    dob = Column(String(10))
    gender = Column(String(1))
    religion = Column(String(50))
    cspan = Column(String(100))
    govtrack = Column(String(100))
    house_history = Column(String(100))
    icpsr = Column(String(100))
    lis = Column(String(100))
    maplight = Column(String(100))
    opensecrets = Column(String(9))
    thomas = Column(String(5))
    votesmart = Column(String(10))
    washington_post = Column(String(100))
    wikipedia = Column(String(100))
    name_first = Column(String(50),nullable=False)
    name_last = Column(String(50),nullable=False)
    official_full = Column(String(100))

class LegTerms(Base):
    __tablename__ = 'leg_terms'
    idn = Column(Integer, primary_key=True)
    bioguideid = Column(String(7), ForeignKey('leg_bio.bioguideid'))
    address = Column(String(255))
    contact_form = Column(String(255))
    district = Column(String(2))
    start = Column(String(10))
    end = Column(String(10))
    office = Column(String(255))
    party = Column(String(50))
    phone = Column(String(12))
    state = Column(String(2),nullable=False)
    ttype = Column(String(3),nullable=False)
    url = Column(String(100))
    leg = relationship(LegBio)

class LegFEC(Base):
    __tablename__ = 'leg_fec'
    fec_id = Column(String(9), primary_key=True)
    bioguideid = Column(String(7), ForeignKey('leg_bio.bioguideid'))
    leg = relationship(LegBio)

if __name__ == '__main__':
    session = sessionmaker()
    build_all_tables(session,'ncj','congress')
