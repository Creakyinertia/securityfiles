from fastapi import  FastAPI
from shared.database import Base , engine
from .routers import users

Desc='''
    _________USERS_________ \n
    1:Get_all_Users_details \n
    2:Get_individual_user_details \n
'''

app = FastAPI(title='Loginbuild',summary="Loginbuild",version='0.0.1',description=Desc)
Base.metadata.create_all(bind=engine)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
