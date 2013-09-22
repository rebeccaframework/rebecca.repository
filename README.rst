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


Repository for SQLAlchemy
-------------------------------------------

basic repository
+++++++++++++++++++++++++++++++++++++++++++++

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
      job = Column(Unicode(255))

Get repository::

  from rebecca.repository.sqla import SQLARepository

  person_repository = SQALRepository(Person, Person.id, DBSession())

this repository for Person model.
To get person, use Person.id as key.


conditional repository
+++++++++++++++++++++++++++++++++++++++++++

repository can configure to set condition::

  person_repository = SQALRepository(Person, Person.id, DBSession(), condition=Person.age>30)


repository factory
+++++++++++++++++++++++++++++++++++++++++++

If you pass the parameters during request time, use factory.

::

  class JobPersonRepository(SQLARepository):
      def __init__(self, db_session, job):
          super(JobPersonRepository, self).__init__(Person, Person.id, dbsession,
                                                    condition=Person.job==job)


The parameter ``job`` will be passed from request attribute.

To register repository factory, add_repository_factory directive::

  config.add_repository_factory(JobPersonRepository, "job-person", args=(DBSession,))

or repository_factory_config decorator::

  @repository_factory_config("job-person", args=(DBSession,))
  class JobPersonRepository(SQLARepository):
      ....


To create repository from registered factory, call create_repository API::

  job = request.matchdict["job"]
  repository = create_repository("person", args=(job,))

Repository for Filesystem
----------------------------------------------

``rebecca.repository.fs.FileSystemRepository`` is repository for FileSystem::

    >>> repository = FileSystemRepository(directory="/path/to/data")
    >>> item = repository.new_item("new-item")
    >>> item.data = b"testing-binary-data"
    >>> import transaction
    >>> transaction.commit()

``FileSystemRepository.new_item`` is create new file system entry.
``item.data`` is binary data that saved in the file.
That's transactional with `transaction <https://pypi.python.org/pypi/transaction>`_ .

.. note::

    ``FileSystemRepository`` uses `repoze.filesafe <https://pypi.python.org/pypi/repoze.filesafe>`_ that not supports py3k yet.


repository interface
---------------------------------------

create object for demonstration::

  person1 = Person(name=u"person1")
  DBSession.add(person1)
  DBSession.flush() # to generate person.id


A repository has dict like interface::

  person_repository[person.id]
  person_repository.get(person.id)

and utility methods::

  person_repository.get_many([1, 2, 3])
  new_person = person_repository.new_item()

pyramid integration
----------------------------------------------

rebecca.repository provides directive for pyramid registry.::

  config.include('rebecca.repository')
  config.add_repository(person_repository, 'person')

or using repository_config decorator::

  @repository_config(name="person", args=(DBSession,))
  class PersonRepository(SQLARepository):
      def __init__(self, dbsession):
          super(PersonRepository, self).__init__(Person, Person.id, dbsession)

To get registered repositories, use get_repository::

  get_repository(request, 'person')
