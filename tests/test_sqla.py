import pytest
from testfixtures import ShouldRaise

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"
    id = sa.Column(sa.Integer, primary_key=True)

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

    def test_key_error(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        with ShouldRaise(KeyError(100)):
            person_repository[100]

    def test_it(self, target, dbsession):
        person_repository = target(Person, 'id', dbsession)
        person = Person()
        dbsession.add(person)
        dbsession.flush()
        result = person_repository[person.id]

        assert result == person
