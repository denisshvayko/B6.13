from bottle import request
from bottle import route
from bottle import run
from bottle import HTTPError
import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "<h1>Всего у {}, {} альбомов:</h1><ul><li>".format(artist, len(albums_list))
        result += "</li><li>".join(album_names)
        result += "</li></ul>"
    return result

@route("/albums", method="POST")
def albumm():
    try:
        album_data = {
            "year": request.forms.get("year"),
            "artist": request.forms.get("artist"),
            "genre": request.forms.get("genre"),
            "album": request.forms.get("album")
        }
        album.year_validation(album_data['year'])
        alb_info = album.checker(album_data)
        if album.album_exist(alb_info):
            resource_path = album.save_user(album_data)
    except (album.BadLength, album.ItsNotDigit) as err:
        return HTTPError(400, str(err))
    except (album.AlreadyExist, album.NotEnoughFilters) as err:
        return HTTPError(409, str(err))
    else:
        print("album saved at: ", resource_path)
        return "Данные успешно сохранены"

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)