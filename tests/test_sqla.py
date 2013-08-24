import pytest
from testfixtures import ShouldRaise

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode(255))

@pytest.fixture
def dbsession(request):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine("sqlite:///")
    Session = sessionmaker()
    session = Session(bind=engine)
    Base.metadata.create_all(bind=engine)
    def fin():
        session.rollback()
        session.close()
    request.addfinalizer(fin)
    return session

class TestSQLARepository(object):

    @pytest.fixture
    def target(self):
        from rebecca.repository.sqla import SQLARepository
        return SQLARepository

    def test_impl(self, target):
        from zope.interface.verify import verifyClass
        from rebecca.repository.interfaces import IRepository
        verifyClass(IRepository, target)

    def test_init_with_str(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        assert person_repository.keyattr == Person.id

    def test_init_with_property(self, target, dbsession):
        person_repository = target(Person, Person.id, dbsession)
        assert person_repository.keyattr == Person.id

    def test_key_error(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        with ShouldRaise(KeyError(100)):
            person_repository[100]

    def test_new_item(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        result = person_repository.new_item()
        dbsession.flush()

        assert person_repository[result.id] == result

    def test_get_item(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        person = Person()
        dbsession.add(person)
        dbsession.flush()
        result = person_repository[person.id]

        assert result == person

    def test_get_slice(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        persons = []
        for i in range(100):
            person = Person()
            persons.append(person)
            dbsession.add(person)
        dbsession.flush()
        result = person_repository[10:20]

        assert len(result) == 10
        assert result == persons[10:20]

    def test_iter(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        persons = []
        for i in range(100):
            person = Person()
            persons.append(person)
            dbsession.add(person)
        dbsession.flush()
        result = list(person_repository)

        assert result == persons

    def test_get(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        person = Person()
        dbsession.add(person)
        dbsession.flush()
        result = person_repository.get(person.id)

        assert result == person

    def test_with_condition(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession,
                                   condition=Person.name==u"testing")

        person1 = Person(name="testing")
        dbsession.add(person1)
        person2 = Person(name="x-testing")
        dbsession.add(person2)
        dbsession.flush()
        result = list(person_repository)

        assert result == [person1]
