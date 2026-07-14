from .utils import *
from routers.auth import get_current_user, get_db, authneticate_user, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db]=override_get_db

def test_authenticate_user(test_user):
    db = testingSessionLocal()
    authUser = authneticate_user(test_user.username,'password', db)
    assert authUser is not None
    assert authUser.username == test_user.username

    invalid_user = authneticate_user('nouser', 'password', db)
    assert invalid_user is False

    invalid_pwd = authneticate_user(test_user.username, 'pwd', db)
    assert invalid_pwd is False

def test_create_access_token():
    usrname='username'
    user_id=1
    role='user'
    expires_delta=timedelta(days=1)

    token = create_access_token(usrname, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature':False})

    assert decoded_token['id'] == user_id
    assert decoded_token['sub'] == usrname
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_current_user_valid():
    usrname='username'
    user_id=1
    role='user'
    expires_delta=timedelta(days=1)

    token = create_access_token(usrname, user_id, role, expires_delta)

    user = await get_current_user(token)

    assert user == {'username': 'username', 'userId': 1, 'role':'user'}

@pytest.mark.asyncio
async def test_current_user_invalid():
    encode = {'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY,algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exinfo:
        await get_current_user(token)

    assert exinfo.value.status_code==401
    assert exinfo.value.detail=='Authrization failed'