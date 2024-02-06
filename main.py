from change_map_size import *
from _3_arrows_keys import *
import pygame
import os


def show_map(params):
    global scale

    map_file = load_map(params)

    # pygame
    pygame.init()
    pygame.display.set_caption('Большой Бублик')
    screen = pygame.display.set_mode((600, 450))

    while True:
        screen.blit(map_file, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                pygame.quit()
                exit(0)

            # Обработка изменения масштабирования (PAGEUP - увеличение, PAGEDOWN - уменьшение):
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    scale, params, map_file = change_map_size(scale, 1, params)

                elif event.key == pygame.K_PAGEDOWN:
                    scale, params, map_file = change_map_size(scale, -1, params)
                else:
                    params, map_file = arrows(params['ll'], params['z'], event.key, params)
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
