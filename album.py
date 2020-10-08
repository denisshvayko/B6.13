import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def checker(album_data):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    for key,value in album_data.items():
        if (key == 'artist' or key == 'album') and value == None:
            print("Дичь")
            raise NotEnoughFilters("Было введено не достаточно параметров")
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == album_data['artist'], Album.album == album_data['album']).all()
    return albums

def year_validation(year):
    if year != None and year.isdigit()==False:
        raise ItsNotDigit("В строке года присутствуют символы помимо чисел")
    elif year != None and len(year)!=4:
        raise BadLength("Введен некорректный год (длина года не менее 4-х символов)")
    return True

def album_exist(albums_data):
    if albums_data == []:
        return "Данный альбом будет добавлен в БД"
    else:
        raise AlreadyExist("Данный альбом уже внесен в базу данных")

def save_user(user_data):
    add_album = Album()
    add_album.year = user_data['year']
    add_album.artist = user_data['artist']
    add_album.genre = user_data['genre']
    add_album.album = user_data['album']
    filename = "Данные сохранены в БД! (В6\B6.13\albums.sqlite3)"
    session = connect_db()
    session.add(add_album)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")
    session.close()
    return filename
    
class InvalidYear(Exception):
    """
    Используется для идентификации некорректных годов
    """
    pass

class ItsNotDigit(InvalidYear):
    """
    Используется для проверки года на наличие символов не равным числам
    """
    pass

class ItsNoneType(InvalidYear):
    """
    Используется для проверки года на тип None
    """
    pass

class BadLength(InvalidYear):
    """
    Используется для проверки года на его длину
    """
    pass

class BdGetChecker(Exception):
    """
    Используется для проверки существования альбома в бд
    """
    pass

class NotEnoughFilters(BdGetChecker):
    """
    Указаны не все фильтры
    """
    pass

class AlreadyExist(BdGetChecker):
    """
    Альбом уже существует
    """
    pass

