import requests
from math import radians, cos, sqrt


def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = radians((a_lat + b_lat) / 2.)
    lat_lon_factor = cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = sqrt(dx * dx + dy * dy)

    return distance


def find_organization(coords, window_coords, scale):
    map_coords = list(map(float, coords.split(',')))
    lat_point = map_coords[0] + (scale[0] / 600) * (window_coords[0] - 300)
    lon_point = map_coords[1] + (scale[1] / 450) * (225 - window_coords[1])

    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": '182b9e48-9043-46cd-acc2-c50e9312a99d',
        "lang": "ru_RU",
        "text": 'аптека',
        "ll": ','.join([str(lat_point), str(lon_point)]),
        "spn": '1,1',
        "type": 'biz'
    }
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    print(response.url)
    if not json_response:
        return False
    if not json_response['features']:
        return False


    organization = json_response["features"][0]
    org_address = organization["properties"]["name"]
    org_cords = ','.join(map(str, organization['geometry']['coordinates']))

    if lonlat_distance((lat_point, lon_point), organization['geometry']['coordinates']) > 50:
        return False

    return org_cords, org_address
