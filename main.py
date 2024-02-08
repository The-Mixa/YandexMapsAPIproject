import requests
import pygame
import sys
import os

from _4_map_type import *
import _4_map_type
from _3_arrows_keys import *
from change_map_size import *
from _11_find_adress import *

from pygame_widgets.button import ButtonArray
import pygame_widgets
from load_map import load_map


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
        onClicks=(lambda: change_map_type('map', params),
                  lambda: change_map_type('sat', params),
                  lambda: change_map_type('skl', params))
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
                    params, map_file = arrows(params['ll'], z_to_spn[str(params['z'])], event.key, params)
            elif event.type == pygame.MOUSEBUTTONDOWN: # ищем объёкт по нажатию мыши
                if event.button == 1: # куда вписывать ещё не знаю, поэтому будет просто строка, что нашлось
                    find_object(params['ll'], pygame.mouse.get_pos(), z_to_spn[str(params['z'])])

        if _4_map_type.CHANGED:
            _4_map_type.CHANGED = False
            response = requests.get(server, params=params)

            if not response:
                print("Ошибка выполнения запроса:")
                print(response.url)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)

            map_file = load_map(params)
        screen.fill('black')
        screen.blit(map_file, (0, 0))

        pygame_widgets.update(events)
        pygame.display.update()

    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    lat, lon = "60.945376", "76.590455"
    scale = int(input('Введите желаемый масштаб от 1 до 20:\n'))
    z_to_spn = {
    '19': (0.0005, 0.0005),
    '18': (0.001, 0.001),
    '17': (0.0015, 0.0015),
    '16': (0.004, 0.004),
    '15': (0.009, 0.009),
    '14': (0.01, 0.01),
    '13': (0.02, 0.02),
    '12': (0.05, 0.05),
    '11': (0.09, 0.09),
    '10': (0.2, 0.2),
    '9': (0.5, 0.5),
    '8': (0.7, 0.7),
    '7': (1.5, 1.5),
    '6': (2.5, 2.5),
    '5': (5, 5),
    '4': (10, 10),
    '3': (20, 20),
    '2': (35, 35)}

    if scale < 1 or scale > 20:
        print('Неверно задан размер')

    else:
        params = {
            'll': ','.join([lon, lat]),
            'z': scale,
            'l': 'map'
        }

show_map(params)
