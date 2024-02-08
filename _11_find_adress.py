import requests
def find_object(coords, window_coords, scale):
    map_coords = list(map(float, coords.split(',')))
    click_coords = (round(scale[0] / 600  * window_coords[0], 6),  round(scale[1] / 450 * window_coords[1], 6))
    crds_on_window = (str(float(map_coords[1] - scale[1] / 2 + click_coords[1])), str(map_coords[0] - scale[0] / 2 + click_coords[0]))
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": '182b9e48-9043-46cd-acc2-c50e9312a99d',
        "lang": "ru_RU",
        "text": ','.join(crds_on_window),
    }
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    if not json_response:
        pass
    object = json_response["features"][0]
    return object


