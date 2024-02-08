from search_object import search_object
from change_map_size import *
import requests
import pygame
import sys
import os

from _4_map_type import *
import _4_map_type
from _3_arrows_keys import *
from change_map_size import *
from _11_find_adress import *

from pygame_widgets.button import ButtonArray, Button
import pygame_widgets
from load_map import load_map


def remove_point(params):
    if 'pt' in params:
        del params['pt']
    _4_map_type.CHANGED = True
    _4_map_type.REMOVED = True


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

    # размеры рамки ввода текста для поиска
    input_bar_width = 240
    input_bar_height = 23

    input_text = ''
    font_input = pygame.font.Font(None, 18)
    font_input_text = font_input.render(input_text, True, 'black')

    font_search = pygame.font.Font(None, 21)
    font_search = font_search.render('Найти', True, 'white')

    scale_font = pygame.font.Font(None, 20)
    scale_text = scale_font.render(f'Масштаб: {scale}', True, 'black')

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
                  lambda: change_map_type('skl', params)),
    )

    remove_button = Button(
        screen, 315, 10, 50, 25,
        text='Cброс', fontSize=18, margin=5,
        textColour=(255, 255, 255),
        inactiveColour=(255, 0, 0),
        hoverColour=(200, 50, 50),
        pressedColour=(200, 100, 100),
        borderThickness=1,
        borderColour='black',
        onClick=lambda: remove_point(params),
    )

    run = True
    while run:
        screen.blit(map_file, (0, 0))
        screen.blit(scale_text, (1, 435))  # отрисовка масштаба

        # отрисовка рамки поиска (с чёрной границей, размером в 1 пиксель)
        pygame.draw.rect(screen, 'black', (9, 9, input_bar_width + 2, input_bar_height + 2))
        pygame.draw.rect(screen, 'white', (10, 10, input_bar_width, 23))
        screen.blit(font_input_text, (10, 15))

        # отрисовка "кнопки поиска" (красный цвет) с текстом
        pygame.draw.rect(screen, 'black', (15 + input_bar_width, 9, 50, input_bar_height + 2))
        pygame.draw.rect(screen, 'red', (16 + input_bar_width, 10, 48, input_bar_height))
        screen.blit(font_search, (15 + input_bar_width + 3, input_bar_height // 2 + 3))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                os.remove('map.png')
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    scale, params, map_file = change_map_size(scale, 1, params)

                elif event.key == pygame.K_PAGEDOWN:
                    scale, params, map_file = change_map_size(scale, -1, params)

                elif event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                    params, map_file = arrows(params['ll'], z_to_spn[str(params['z'])], event.key, params)

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                # Добавление 1 символа в строку поиска
                else:
                    input_text += event.unicode

                # Постоянно обновляем строку поиска (отображаем только первые 28 символов запроса)
                font_input_text = font_input.render(input_text[:28], True, 'black')
                scale_text = scale_font.render(f'Масштаб: {scale}', True, 'black')

            # Обработка нажатия ЛКМ (на клавишу поиска):
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()

                # Выполняем поиск:
                if x in range(15 + input_bar_width, 15 + input_bar_width + 50 + 1) and \
                        y in range(9, 9 + input_bar_height + 2):
                    try:
                        params, map_file = search_object(input_text, params)
                    except Exception as e:
                        print('error', e)
                else:
                    cords, address = find_object(params['ll'], pygame.mouse.get_pos(), z_to_spn[str(params['z'])])
                    params['pt'] = f'{cords},pm2rdm'
                    input_text = address
                    font_input_text = font_input.render(input_text[:28], True, 'black')
                    _4_map_type.CHANGED = True


        if _4_map_type.CHANGED:
            _4_map_type.CHANGED = False
            response = requests.get(server, params=params)

            if not response:
                print("Ошибка выполнения запроса:")
                print(response.url)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)

            map_file = load_map(params)

            if _4_map_type.REMOVED:
                _4_map_type.REMOVED = False
                input_text = ''
                font_input_text = font_input.render(input_text[:28], True, 'black')

        pygame_widgets.update(events)
        pygame.display.update()

    pygame.quit()

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
