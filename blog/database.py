from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#echo→SQLAlchemyロギングを設定するためのショートカットであり、Pythonの標準loggingモジュールを介して実行されます。
SQLALCHEMY_DATABASE_URL = ("sqlite:///./blog.db , echo = True")
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()