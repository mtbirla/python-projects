from .utils import *
from routers.admin import get_current_user, get_db

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_curr_user

def test_read_all(test_todo):
    response = client.get('/admin/todo')
    assert response.status_code==200
    assert response.json() == [{'title' : 'test', 'description':'test desc', 'priority':1, 'completed':False, 'owner_id':1, 'id': 1}]