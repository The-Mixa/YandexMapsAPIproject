import requests
from load_map import load_map

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

def get_postal_code(address, par):
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json",
        "ll": par["ll"]
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

    # почтовый индекс
    try:
        postal_code = f'[Индекс: {toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]}]'
    except:
        postal_code = '[Индекс не найден]'

    return postal_code


def handler(address, par):
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json",
        "ll": par["ll"]
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

    # адрес объекта
    try:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
    except:
        toponym_address = ''

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]

    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        'z': 2,
        "l": "map",
        "pt": f'{",".join([toponym_longitude, toponym_lattitude])},pm2rdm'
    }

    return map_params, toponym_address


# Поиск объекта и его отображение
def search_object(search, params):
    _params, add_ = handler(search, params)
    _params['z'] = params['z']

    return _params, load_map(_params), add_
