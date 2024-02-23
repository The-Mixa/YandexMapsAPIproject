# Блок PyGame
from pygame_widgets.button import ButtonArray, Button  # виджеты PyGame - группа кнопок, кнопки
import pygame_widgets  # обновление виджетов PyGame
import pygame
import sys  # закрытие программы (завершение работы)
import os  # удаление изображения (карты)

# Далее - импорт функций для каждого задания
# (1, 7, ... задания находятся в этом файле - main.py)

# 2 задание
from change_map_size import *
from load_map import load_map  # Функция загрузки изображения-карты

# 3 задание
from _3_arrows_keys import *

# 4 задание
from _4_map_type import *
import _4_map_type

# 5 задание
from search_object import *

# 11 задание (вопрос возник - зачем 2 коммита?)
from _11_find_adress import *

import requests

#12 задание
from _12_find_org import *


def is_response_incorrect(resp):
    if not resp:
        print("Ошибка выполнения запроса:")
        print(resp.url)
        print("Http статус:", resp.status_code, "(", resp.reason, ")")
        sys.exit(1)


# Удалить метку с карты
def remove_point(params):
    global is_removed
    is_removed = True

    if 'pt' in params:
        del params['pt']
    _4_map_type.CHANGED = True
    _4_map_type.REMOVED = True



# изменение текста, отображающего адрес указанной метки (или при завершении поиска объекта)
def change_address_text(address):
    if len(address) > 55:
        add_1, add_2 = address[:54] + '-', address[54:]
        return font_address.render(add_1, True, 'black'), font_address.render(add_2, True, 'black')
    return font_address.render(address, True, 'black'), font_address.render('', True, 'black')

# Отображение карты
def show_map(params):
    global scale, font_address, is_removed
    server = 'http://static-maps.yandex.ru/1.x/'
    is_removed = False
    response = requests.get(server, params=params)
    is_response_incorrect(response)

    map_file = load_map(params)

    # pygame
    pygame.init()
    pygame.display.set_caption('Большой Бублик')
    screen = pygame.display.set_mode((600, 450))

    # размеры рамки ввода текста для поиска
    input_bar_width = 240
    input_bar_height = 23

    # поиск объекта
    input_text = ''
    font_input = pygame.font.Font(None, 18)
    font_input_text = font_input.render(input_text, True, 'black')

    # шрифт для кнопки поиска
    font_search = pygame.font.Font(None, 21)
    font_search = font_search.render('Найти', True, 'white')

    # шрифт для отображения текущего масштаба карты (по параметру z)
    scale_font = pygame.font.Font(None, 20)
    scale_text = scale_font.render(f'Масштаб: {scale}', True, 'black')

    # флаг (почтовый индекс - 9 задание) и шрифт для переключателя
    _get_post_index = False
    post_font = pygame.font.Font(None, 18)
    post_text = post_font.render('Индекс', True, 'white')

    # шрифт для отображения адреса найденного объекта
    address_bar_width = 354
    font_address = pygame.font.Font(None, 16)
    font_address_text1 = font_address.render('', True, 'black')
    font_address_text2 = font_address.render('', True, 'black')  # перенос строки

    buttons = ButtonArray(
        screen,
        515, 10, 80, 100, (1, 3),
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
        screen, 315, 9, 50, 25,
        text='Сброс', fontSize=18, margin=5,
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
        # если была нажата кнопка сброса - очищаем поле вывода адреса
        if is_removed:
            font_address_text1, font_address_text2 = change_address_text('')
            is_removed = False

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

        # отрисовка кнопки-переключателя (для отображения почтового индекса)
        post_button_color = 'green' if _get_post_index else 'red'
        pygame.draw.rect(screen, 'black', (375, 9, 50, input_bar_height + 2))
        pygame.draw.rect(screen, post_button_color, (376, 10, 48, input_bar_height))
        screen.blit(post_text, (377, 16))

        # отрисовка информации об объекте:
        pygame.draw.rect(screen, 'black', (9, 39, address_bar_width + 2, input_bar_height * 2 + 2))
        pygame.draw.rect(screen, 'white', (10, 40, address_bar_width, input_bar_height * 2))
        screen.blit(font_address_text1, (10, 45))
        screen.blit(font_address_text2, (10, 65))

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                os.remove('map.png')
                run = False
            elif event.type == pygame.KEYDOWN:

                # Увеличение масштаба карты
                if event.key == pygame.K_PAGEUP or event.key == pygame.K_p:
                    scale, params, map_file = change_map_size(scale, 1, params)

                # Уменьшение масштаба карты
                elif event.key == pygame.K_PAGEDOWN or event.key == pygame.K_o:
                    scale, params, map_file = change_map_size(scale, -1, params)

                # Перемещение карты (при нажатии стрелочек)
                elif event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                    params, map_file = arrows(params['ll'], z_to_spn[str(params['z'])], event.key, params)

                # Удаление одного символа из строки поиска
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                # Добавление 1 символа в строку поиска
                else:
                    input_text += event.unicode

                # Постоянно обновляем строку поиска (отображаем только первые 28 символов запроса)
                font_input_text = font_input.render(input_text[:28], True, 'black')
                scale_text = scale_font.render(f'Масштаб: {scale}', True, 'black')

            # Обработка нажатия ЛКМ (на клавишу поиска):
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()

                    # Выполняем поиск:
                    if x in range(15 + input_bar_width, 15 + input_bar_width + 50 + 1) and \
                            y in range(9, 9 + input_bar_height + 2):
                        try:
                            params, map_file, add_ = search_object(input_text, params)
                            postal_code = get_postal_code(input_text, params)

                            if not _get_post_index:
                                postal_code = ''

                            font_address_text1, font_address_text2 = change_address_text(add_ + f' {postal_code}')

                        except Exception as e:
                            font_address_text1, font_address_text2 = change_address_text('Ничего не найдено')
                            print('error:', e)

                    elif x in range(376, 376 + 48 + 1) and y in range(9, 9 + input_bar_height + 2):
                        _get_post_index = not _get_post_index

                    else:
                        if not(x in range(9, 376 + 48 + 1) and y in range(10, 85 + 1)):
                            try:
                                cords, add_ = find_object(params['ll'], pygame.mouse.get_pos(), z_to_spn[str(params['z'])])
                                postal_code = get_postal_code(add_, params)

                                if not _get_post_index:
                                    postal_code = ''

                                params['pt'] = f'{cords},pm2rdm'

                                font_address_text1, font_address_text2 = change_address_text(add_ + f' {postal_code}')

                                _4_map_type.CHANGED = True
                            except Exception as e:
                                print('error:', e)

                # find organization by right click
                elif event.button == 3:
                    data = find_organization(params['ll'], pygame.mouse.get_pos(), z_to_spn[str(params['z'])])
                    if data:
                        cords, add_ = data
                        params['pt'] = f'{cords},pm2rdm'
                        font_address_text1, font_address_text2 = change_address_text(add_)
                        _4_map_type.CHANGED = True
                    else:
                        font_address_text1, font_address_text2 = change_address_text('')
                        del params['pt']


        #
        if _4_map_type.CHANGED:
            _4_map_type.CHANGED = False
            response = requests.get(server, params=params)
            is_response_incorrect(response)

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
    scale = 15  # int(input('Введите желаемый масштаб от 1 до 20:\n'))
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
