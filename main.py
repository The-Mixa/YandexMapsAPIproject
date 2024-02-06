from search_object import search_object
from change_map_size import *
import pygame
import os


def show_map(params):
    global scale

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

    while True:
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                pygame.quit()
                exit(0)

            # Обработка нажатия клавиатуры:
            elif event.type == pygame.KEYDOWN:

                # Увеличение масштаба карты на 1:
                if event.key == pygame.K_PAGEUP:
                    scale, params, map_file = change_map_size(scale, 1, params)

                # Уменьшение масштаба карты на 1:
                elif event.key == pygame.K_PAGEDOWN:
                    scale, params, map_file = change_map_size(scale, -1, params)

                # Удаление 1 символа из строки поиска
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

            pygame.display.flip()


if __name__ == '__main__':
    lat, lon = input('Введите кординаты (<широта>, <долгота>): ').split(', ')
    scale = int(input('Введите желаемый масштаб от 1 до 20:'))

    if scale < 1 or scale > 20:
        print('Неверно задан размер')

    else:
        params = {
            'll': ','.join([lon, lat]),
            'z': scale,
            'l': 'map'
        }

        show_map(params)
