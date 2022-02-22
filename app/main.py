from charset_normalizer import models
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from fastapi import Depends, FastAPI
from .routers import post,user
   
models.Base.metadata.create_all(bind = engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database='fastapi',
        user='postgres',password='Test12341!',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection succesful")
        break
    except Exception as error:
        print("connection failed")
        print("Error: ",error)
        time.sleep(2)


my_post = [{"title":"title 1","content":"content1","id":1},{"title":"title 2","content":"content2","id":2}]

def find_post(id):
    for p in my_post:
        if p['id']==id:
            return p
 
def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message":"Hello World"}