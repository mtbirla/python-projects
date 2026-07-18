from fastapi import FastAPI
import models
from Core.database import engine
from routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine) #this will only run if todo doesn't exist

@app.get("/healthy")
def check_health():
    return {'Status': 'OK'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)