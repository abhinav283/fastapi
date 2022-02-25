from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#when you wany to talk DB you have create session

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine) 

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost',database='fastapi',
#         user='postgres',password='Test12341!',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection succesful")
#         break
#     except Exception as error:
#         print("connection failed")
#         print("Error: ",error)
#         time.sleep(2)
        