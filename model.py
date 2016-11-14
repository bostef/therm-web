#!/usr/bin/env python
#
#  SQLAlchemy database model.  This defines your database using SQLAlchemy
#  "declarative" format.  See:
#
#      http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/declarative.html
#
#  for more information
#
#  See the sections marked with "XXX" to customize for your application.
#  Or remove this file and references to "model" if you aren't using a
#  database.
#
#  See the README.md for more information
#
#  Written by Sean Reifschneider <jafo@jafo.ca>, 2013
#
#  Part of the python-bottle-skeleton project at:
#
#      https://github.com/linsomniac/python-bottle-skeleton
#
#  I hereby place this work, python-bottle-wrapper, into the public domain.

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import event, Column, Integer, String, ForeignKey, Time, Float, Date
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.orm import relationship, backref
from sqlalchemy.pool import Pool
from datetime import time, date

def initdb():
    '''Populate an empty database with the schema'''
    from lib.bottledbwrap import dbwrap

    dbwrap.connect()
    dbwrap.Base.metadata.create_all()


@event.listens_for(Pool, 'checkout')
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    '''Ping a database connection before using it to make sure it is still
    alive.'''
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute('SELECT 1')
    except:
        # optional - dispose the whole pool instead of invalidating separately
        # connection_proxy._pool.dispose()

        # pool will try connecting again up to three times before raising.
        raise DisconnectionError()
    cursor.close()


#  XXX Your model goes here
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)

    name = Column(String(length=20), nullable=False)
    full_name = Column(String(length=60), nullable=False)
    email_address = Column(String(length=60), nullable=False)

class CyclePlanning(Base):  # lien entre un cycle et des plannings
    __tablename__ = 'cycle_planning'
    #id = Column(Integer(), primary_key=True, autoincrement=True)
    cycle_id = Column(Integer, ForeignKey('cycle.cycle_id'), primary_key=True)
    planning_id = Column(Integer, ForeignKey('planning_jour.planning_id'), primary_key=True)
    position = Column(Integer(), primary_key=True)
    planning = relationship("PlanningJour", back_populates="cycles")
    cycle = relationship("Cycle", back_populates="plannings")


class PlanningJour(Base):
    __tablename__='planning_jour'
    planning_id = Column(Integer(), primary_key=True)
    libelle = Column(String(length=40), nullable=False)
    cycles = relationship("CyclePlanning", back_populates="planning")

    def __repr__(self):
        return "<PlanningJour(libelle='%s')>" % self.libelle


class Plage(Base):
    __tablename__ = 'plage'
    plage_id = Column(Integer(), primary_key=True)
    heure = Column(Time(), nullable=False)
    temperature = Column(Float(), nullable=False)
    jour_id = Column(ForeignKey('planning_jour.planning_id'))
    jour = relationship("PlanningJour", back_populates="plages")
    def __repr__(self):
        return "<Plage(planning=%s, heure='%s',t=%s)>" % (self.jour, self.heure, self.temperature)


PlanningJour.plages = relationship("Plage", order_by = Plage.heure, back_populates = "jour", cascade="all, delete-orphan")

class Cycle(Base):
    __tablename__ = 'cycle'
    cycle_id = Column(Integer(), primary_key=True)
    libelle = Column(String(length=40), nullable=False)
    plannings = relationship("CyclePlanning", back_populates="cycle", order_by=CyclePlanning.position, cascade="all, delete-orphan")

    def __repr__(self):
        return "<Cycle(libelle=%s)>" % (self.libelle)


class AffectationCycle(Base):
    __tablename__= 'affectation_cycle'
    affectation_id = Column(Integer(), primary_key=True)
    debut = Column(Date(), nullable=False)
    fin = Column(Date())
    cycle_id = Column(ForeignKey('cycle.cycle_id'), nullable=False)
    cycle = relationship('Cycle')

    def __repr__(self):
        return "<AffectationCycle(Debut=%s, cycle=%s)>" % (self.debut, self.cycle)


#  XXX A database-related function
def user_by_name(name):
    from lib.bottledbwrap import dbwrap
    db = dbwrap.session()
    user = db.query(User).filter_by(name=name).first()
    return user


#  XXX Some sample data for testing the site
def create_sample_data():
    from lib.bottledbwrap import dbwrap

    dbwrap.connect()
    dbwrap.Base.metadata.create_all()
    db = dbwrap.session()

    """
    sean = User(
            full_name='Sean Reifschneider', name='sean',
            email_address='jafo@example.com')
    db.add(sean)
    evi = User(
            full_name='Evi Nemeth', name='evi',
            email_address='evi@example.com')
    db.add(evi)
    dmr = User(
            full_name='Dennis Ritchie', name='dmr',
            email_address='dmr@example.com')
    db.add(dmr)
    """
    matin = PlanningJour(libelle="Un autre Matin")
    matin.plages=[ Plage(heure=time(8,0,0), temperature=25.0),
                                                    Plage(heure=time(18, 0, 0), temperature=25.0)]
    db.add(matin)

    ferie = PlanningJour(libelle="Férié &")
    ferie.plages=[ Plage(heure=time(8,30,0), temperature=22.0),
                                                    Plage(heure=time(17, 0, 0), temperature=23.0)]
    db.add(ferie)


    cycle = Cycle(libelle="un autre cycle")

    planning = CyclePlanning(position=1)
    planning.planning = matin
    cycle.plannings.append(planning)

    planning = CyclePlanning(position=2)
    planning.planning = matin
    cycle.plannings.append(planning)
    db.add(cycle)


    affectation = AffectationCycle(debut=date(2016,1,1), cycle=cycle)
    db.add(affectation)

    db.commit()
