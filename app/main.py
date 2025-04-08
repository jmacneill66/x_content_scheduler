from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import database, schemas, crud
from .tasks import post_scheduled_content
from typing import List  # Make sure to import List

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

@app.post("/schedule/", response_model=schemas.Post)
def schedule_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    db_post = crud.create_post(db=db, post=post)
    post_scheduled_content.apply_async((db_post.id,), eta=db_post.scheduled_time)
    return db_post

@app.get("/posts/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db)):
    posts = crud.get_posts(db=db)
    return posts