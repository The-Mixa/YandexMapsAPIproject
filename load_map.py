import requests
from pygame import image


# функция для загрузки изображения (pygame)
def load_map(params):
    try:

        server = 'http://static-maps.yandex.ru/1.x/'
        response = requests.get(server, params=params)

        if not response:
            return f'Ошибка {response.status_code}: {response.reason}'

        # загрузка изображения
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

        return image.load(map_file)

    except Exception as e:
        return f'Ошибка при исполнении программы: {e}'
