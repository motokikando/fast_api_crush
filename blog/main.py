from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from .import models
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from typing import List




app = FastAPI()

#modelsのデータベースを構築する
models.Base.metadata.create_all(engine)


#データベースの生成とdbをSessionLoacalと定義
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog')
#schemasファイルからclassのBlogを取り出す
#FastAPI のDepends
#requestはHTTPメソッドの呼び起こしで使う
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    #modelsファイルのBlogクラスのtitle, bodyカラムをrequest
    new_blog = models.Blog(title=request.title, body = request.body)
    #dbにnew_blogを追加
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#全件取得　
#response を201のオリジナルに指定
#複数の
@app.get('/blog', response_model = List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


#idを表示しないでtitleとbodyのみ取得
@app.get('/blog/{id}', status_code = 200, response_model = schemas.ShowBlog)
def show(id, response: Response , db: Session = Depends(get_db)):
    #queryで指定されたid一件のみを取得
    #blogにmodels.Blogs.idをidとしてqueryにする
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail =  f"Blog with the id {id} is not available")
        #queryに指定されたidが存在しないとき404エラーを返す
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with the id {id} is not available"}

    return blog

@app.delete('/blog/{id}', status_code= status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    #消去するときは必ずdbにコミットをする
    db.commit()

    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update(request)
    db.commit()
    return 'updated'

@app.get('/blog', status_code=status.HTTP_201_CREATED)
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
