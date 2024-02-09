import requests


def find_object(coords, window_coords, scale):
    map_coords = list(map(float, coords.split(',')))
    lat_point = map_coords[0] + (scale[0] / 600) * (window_coords[0] - 300)
    lon_point = map_coords[1] + (scale[1] / 450) * (225 - window_coords[1])
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": '182b9e48-9043-46cd-acc2-c50e9312a99d',
        "lang": "ru_RU",
        "text": ','.join([str(lon_point), str(lat_point)]),
    }
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    if not json_response:
        pass

    organization = json_response["features"][0]
    org_address = organization["properties"]["GeocoderMetaData"]["text"]
    org_cords = ','.join(map(str, organization['geometry']['coordinates']))
    return org_cords, org_address