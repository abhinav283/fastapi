from .. import models,schemas
from fastapi import FastAPI, Depends, Response,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db

router = APIRouter(
    prefix="/posts",
    tags=['POSTS']
)

@router.get("/")
def get_posts(db:Session=Depends(get_db)):
    # cursor.execute("""select * from posts""" )
    # posts=cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,published) values(%s,%s,%s) RETURNING *  """, (post.title,post.content,post.published))  
    # new_post =cursor.fetchone()  
    # conn.commit()
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}
 
@router.get("/{id}") #path parameter
def get_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""select * from posts where id=%s """, (str(id)))
    # post= cursor.fetchone() 
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return{"post_Details":post}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT ) 
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