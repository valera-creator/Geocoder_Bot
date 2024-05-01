import requests


def get_image(city):
    coords = get_coords(city)
    link = 'http://static-maps.yandex.ru/1.x/'
    search_params = {
        'll': coords,
        'spn': '0.6,0.6',
        'l': 'map',
        'pt': f'{coords},pm2lbm'
    }
    response = requests.get(link, params=search_params)

    # Запишем полученное изображение в файл.

    with open("image.png", "wb") as file:
        file.write(response.content)


def get_coords(search_object):
    params_search = {
        "geocode": search_object,
        "format": "json",
        "apikey": '320ef2a1-88df-49be-a524-bffd6f29cf76'
    }
    link = 'http://geocode-maps.yandex.ru/1.x/'
    response = requests.get(link, params=params_search)
    data = response.json()
    return ','.join(data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split())


def check_get_image(search_object):
    """
    функция вернет True, если место нашлось. Это сделано, чтобы потом различить,
    отобразить картинку города или картинку того, что город не найден
    """
    try:
        get_image(search_object)
        return True
    except Exception:
        return False
