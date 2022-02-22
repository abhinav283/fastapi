from typing import Optional
from charset_normalizer import models
from fastapi import Depends, FastAPI,Response,status,HTTPException
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas 
from .database import engine,get_db
from sqlalchemy.orm import Session

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


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts(db:Session=Depends(get_db)):
    # cursor.execute("""select * from posts""" )
    # posts=cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,published) values(%s,%s,%s) RETURNING *  """, (post.title,post.content,post.published))  
    # new_post =cursor.fetchone()  
    # conn.commit()
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}
 
@app.get("/posts/{id}") #path parameter
def get_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""select * from posts where id=%s """, (str(id)))
    # post= cursor.fetchone() 
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return{"post_Details":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT ) 
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute(""" delete from posts where id=%s returning *""" ,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found" )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")#,status_code=status.HTTP_204_NO_CONTENT ) 
def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute(""" update posts set title = %s,content=%s,published=%s  where id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found" )
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}

   
 