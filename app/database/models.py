from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    name = Column(String)
    surname = Column(String)
    clas = Column(String)
    phone = Column(String)
    role = Column(String, default='user')
    lang = Column(String, default='rus')
    hurry = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    genre = Column(String, nullable=True)
    page = Column(String, nullable=True)
    fre = Column(Boolean, default=False)
    mainMes = Column(Integer, nullable=True)
    one = Column(Integer, nullable=True)
    two = Column(Integer, nullable=True)
    three = Column(Integer, nullable=True)
    ziro = Column(String, nullable=True)

class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)
    author = Column(String)
    description = Column(String)
    amount = Column(String)
    link = Column(String, nullable=True)
    mes_id = Column(Integer, nullable=True)

class Trade(Base):
    __tablename__ = 'trades'

    trade_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    book_id = Column(Integer)
    book_name = Column(String)
    status = Column(String)
    date_taking = Column(String)
    date_return = Column(String)

def init_db(database_url: str = "sqlite:///db.sqlite"):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine) 