from fastapi import FastAPI, Depends
from . import schemas, models
from database import engine, SessionLoacal
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn


models.Base.metadata.create_all(engine)


app = FastAPI()

#ローカルホストにパスを追加
@app.get('/blog')
#パラメーターの定義
def index(limit=10, published: bool = True, sort: Optional[str] = None):

    #only get 10published blogs
    return published

    if published:
        return {"data": f'{limit} published blogs from the db'}

    else:
        return {"data": f'{limit} blogs from the db'}


#ローカルホストに/about　ページを追加　
#http://localhost:8000/blog/{id}→対応する　'data':id に変化する

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished'}


@app.get('/blog/{id}')
#idはint型に定義　もしくはstr
def show(id: int):
    #featch blog with id = id
    return{'data': id}

@app.get('/blog/{id}/comments')

def comments(id, limit=10):
    # fetch comments of blog with id = id

    return {'data': {'1', '2'}}

class  Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

def get_db():
    db = SessionLoacal()
    try:
        yield db
    finally:
        db.close()





@app.post('/blog')
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return db

# if __name__ == "__main__":
#     uvicorn.run(app, host='127.0.0.1', port=9000)