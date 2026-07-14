from routers.todos import get_db, get_current_user
from fastapi import status
from .utils import *

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_curr_user

def test_Read_all(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title' : 'test', 'description':'test desc', 'priority':1, 'completed':False, 'owner_id':1, 'id': 1}]

def test_Read_byId(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title' : 'test', 'description':'test desc', 'priority':1, 'completed':False, 'owner_id':1, 'id': 1}

def test_read_byid_not_found():
    response = client.get("/todo/11111")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'No todo found'}

def test_create_todo(test_todo):
    request = {
        'title' : 'title', 'description':'descri', 'priority':3, 'completed':True
    }
    response = client.post('/todo', json=request)
    assert response.status_code == status.HTTP_201_CREATED

    db = testingSessionLocal()
    model = db.query(Todo).filter(Todo.id==2).first()
    assert model.title == request.get('title')

def test_update_todo(test_todo):
    request = {
        'title' : 'title', 'description':'descri', 'priority':3, 'completed':True
    }

    response = client.put('/todo/1', json=request)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = testingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model.title == request.get('title')

def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code==204
    db = testingSessionLocal()
    model = db.query(Todo).filter(Todo.id==1).first()
    assert model is None

def test_delete_todo_not_found():
    response = client.delete('/todo/11111')
    assert response.status_code==404
    assert response.json()=={'detail': 'No todo found to delete'}