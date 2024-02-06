import requests
import pygame
import sys
import os

import _4_map_type
from pygame_widgets.button import ButtonArray
import pygame_widgets

def show_map(params):
    global scale
    server = 'http://static-maps.yandex.ru/1.x/'

    response = requests.get(server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = load_map(params)

    # pygame
    pygame.init()
    pygame.display.set_caption('Большой Бублик')
    screen = pygame.display.set_mode((600, 450))

    buttons = ButtonArray(
        screen,
        510, 10, 80, 80, (1, 3),
        texts=('карта', "спутник", "гибрид"), fontSizes=(13, 13, 13), margins=(3, 3, 3),
        inactiveColour=(155, 155, 155),
        hoverColour=(180, 180, 180),
        pressedColour=(200, 200, 200),

        radiuses=(3, 3, 3),
        border=3,
        onClicks=(lambda: _4_map_type.change_map_type('map', params),
                  lambda: _4_map_type.change_map_type('sat', params),
                  lambda: _4_map_type.change_map_type('skl', params))
    )

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
                # Обработка изменения масштабирования (PAGEUP - увеличение, PAGEDOWN - уменьшение):
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    scale, params, map_file = change_map_size(scale, 1, params)

            elif event.key == pygame.K_PAGEDOWN:
                scale, params, map_file = change_map_size(scale, -1, params)
            else:
                params, map_file = arrows(params['ll'], params['z'], event.key, params)


        if _4_map_type.CHANGED:
            _4_map_type.CHANGED = False
            response = requests.get(server, params=params)
            print(params)

            if not response:
                print("Ошибка выполнения запроса:")
                print(response.url)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)

            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
        screen.fill('black')
        screen.blit(pygame.image.load(map_file), (0, 0))

        pygame_widgets.update(events)
        pygame.display.update()

    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    lat, lon = input('Введите кординаты (<широта>, <долгота>):\n').split(', ')
    scale = int(input('Введите желаемый масштаб от 1 до 20:\n'))

    if scale < 1 or scale > 20:
        print('Неверно задан размер')

    else:
        params = {
            'll': ','.join([lon, lat]),
            'z': scale,
            'l': 'map'
        }

show_map(params)
