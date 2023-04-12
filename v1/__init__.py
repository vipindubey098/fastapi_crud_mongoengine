from fastapi import FastAPI
import mongoengine
from v1.routes import router


app = FastAPI()
app.include_router(router)

mongoengine.connect(db="task2", host="localhost", port=27017)