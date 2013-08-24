.. contents::

.. image:: https://travis-ci.org/rebeccaframework/rebecca.repository.png?branch=master
   :target: https://travis-ci.org/rebeccaframework/rebecca.repository

rebecca.repository
===========================

An implementation of repository pattern for SQLAlchemy.


Getting Started
-------------------------------

install by pip::

  $ pip install rebecca.repository


Implement your model by SQLAlchemy::

  from sqlalchemy import Column, Integer, Unicode
  from sqlalchemy.ext.declarative import declarative_base

  Base = declarative_base()
  DBSession = scoped_session(sessionmaker())

  class Person(Base):
      __tablename__ = "person"
      id = Column(Integer, primary_key=True)
      name = Column(Unicode(255))
      age = Column(Integer, default=0)

Get repository::

  from rebecca.repository.sqla import SQLARepository

  person_repository = SQALRepository(Person, Person.id, DBSession())

this repository for Person model.
To get person, use Person.id as key.

basic dict interface
---------------------------------------

create object for demonstration::

  person1 = Person(name=u"person1")
  DBSession.add(person1)
  DBSession.flush() # to generate person.id


A repository has dict like interface::

  person_repository[person.id]
  person_repository.get(person.id)


conditional repository
------------------------------------------

repository can configure to set condition::

  person_repository = SQALRepository(Person, Person.id, DBSession(), condition=Person.age>30)
