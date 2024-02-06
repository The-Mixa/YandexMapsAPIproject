import requests
from load_map import load_map


# Изменение размеров масштабирования (учитывая допустимые значения)
def change_scale(scl, step):
    if (scl + step < 1) or (scl + step > 20):
        return scl
    return scl + step


# Изменение месштаба карты (параметры: scl: масштаб (1 < scl < 20), step - уменьшение / увеличение масштаба на 1 ед.,
# params - параметры поиска
def change_map_size(scl, step, params):
    scl = change_scale(scl, step)
    params['z'] = scl

    return scl, params, load_map(params)
