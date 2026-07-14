from .utils import *
from routers.users import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_curr_user

def test_user_all(test_user):
    response = client.get('/users')
    assert response.status_code==status.HTTP_200_OK

def test_change_pwd(test_user):
    request = {
        'password' : 'asdfg',
        'new_password': 'Pass@123'
    }
    response = client.put('/users/change-password', json=request)
    assert response.status_code==202

    db=testingSessionLocal()
    model = db.query(Users).filter(Users.id==1).first()
    assert model is not None