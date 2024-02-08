import pygame
from load_map import load_map


def arrows(coords, scale, key, params):
    coords_of_pont = [float(i) for i in coords.split(',')]

    match key:
        case pygame.K_DOWN:
            params['ll'] = f'{coords_of_pont[0]},{coords_of_pont[1] - scale[1]}'
        case pygame.K_UP:
            params['ll'] = f'{coords_of_pont[0]},{coords_of_pont[1] + scale[1]}'
        case pygame.K_LEFT:
            params['ll'] = f'{coords_of_pont[0] - scale[0]},{coords_of_pont[1]}'
        case pygame.K_RIGHT:
            params['ll'] = f'{coords_of_pont[0] + scale[0]},{coords_of_pont[1]}'
    return params, load_map(params)
