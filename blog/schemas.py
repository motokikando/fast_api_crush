from pydantic import BaseModel
from typing import Optional
from .database  import Base


class  Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

#response model を返すクラス
#設定としてormをtrueにしておかないとクエリと繋がらない
class ShowBlog(Blog):
    class Config():
        orm_mode = True

