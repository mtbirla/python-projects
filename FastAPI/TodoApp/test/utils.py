from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from fastapi.testclient import TestClient
import pytest
from models import Todo,Users
from main import app
from routers.auth import bcrypt_context

SQLALCHEMY_DB_URL="sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

testingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=testingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_curr_user():
    return {'username':'mitultest', 'userId':1, 'role':'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todo(
        title = "test",
        description="test desc",
        priority=1,
        completed=False,
        owner_id=1
    )

    db = testingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("Delete from todo;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        email = 'email',
        username = 'mitultest',
        first_name = 'fname',
        last_name = 'lname',
        hashed_pwd = bcrypt_context.hash('password'),
        role = 'admin',
        phone_number = '9876543210'
    )

    db = testingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("Delete from users;"))
        connection.commit()