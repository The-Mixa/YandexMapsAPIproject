from pygame_widgets.button import Button


def change_map_type(typ, params):
    global CHANGED
    params['l'] = typ
    CHANGED = True


CHANGED = False

