import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    tg_id = sqlalchemy.Column(sqlalchemy.String,
                              primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    clas = sqlalchemy.Column(sqlalchemy.String)
    phone = sqlalchemy.Column(sqlalchemy.String)
    role = sqlalchemy.Column(sqlalchemy.String)
    genre = sqlalchemy.Column(sqlalchemy.String)
    fre = sqlalchemy.Column(sqlalchemy.Boolean)
    page = sqlalchemy.Column(sqlalchemy.String)
    mainMes = sqlalchemy.Column(sqlalchemy.String)
    ziro = sqlalchemy.Column(sqlalchemy.String)
    one = sqlalchemy.Column(sqlalchemy.String)
    two = sqlalchemy.Column(sqlalchemy.String)
    three = sqlalchemy.Column(sqlalchemy.String)
    hurry = sqlalchemy.Column(sqlalchemy.Integer)
    xp = sqlalchemy.Column(sqlalchemy.Integer)
    lang = sqlalchemy.Column(sqlalchemy.String)

class Book(SqlAlchemyBase):
    __tablename__ = 'books'
    book_id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    genre = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    link = sqlalchemy.Column(sqlalchemy.String)
    amount = sqlalchemy.Column(sqlalchemy.Integer)
    mes_id = sqlalchemy.Column(sqlalchemy.String)


class trade(SqlAlchemyBase):
    __tablename__ = 'trades'
    trade_id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    date_taking = sqlalchemy.Column(sqlalchemy.String)
    date_return = sqlalchemy.Column(sqlalchemy.String)
    book_id = sqlalchemy.Column(sqlalchemy.Integer)
    book_name = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String)
