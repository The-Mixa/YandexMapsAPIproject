import requests
import pygame
import sys
import os


def show_map(params):
    server = 'http://static-maps.yandex.ru/1.x/'

    response = requests.get(server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    os.remove(map_file)


print('Введите кординаты (<широта>, <долгота>)')
lat, lon = input().split(', ')
print('Введите желаемый масштаб от 1 до 20')
scale = int(input())

params = {
    'll': ','.join([lon, lat]),
    'z': scale,
    'l': 'map'
}

show_map(params)
