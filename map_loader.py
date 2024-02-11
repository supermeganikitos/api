import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import requests

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def make_static_maps_response(someval, delta, map_or_sat, *pt):
    delta = str(delta)
    map_params = {
        "ll": ",".join((str(someval[0]), str(someval[1]))),
        "spn": ",".join([delta, delta]),
        "l": map_or_sat
    }
    if pt:
        map_params['pt'] = '~'.join((','.join(i) for i in pt))
        print(map_params['ll'])
        print(map_params['pt'])
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def blit_amg(map_file):
    scr1 = pygame.image.load(map_file)
    screen.blit(scr1, (0, 50))


someval = [37.617698, 55.755864]
delta = 0.2
map_sat_hyb = 'map'
map_file = make_static_maps_response(someval, delta, map_sat_hyb)
pygame.init()
pygame.display.set_caption('Карта')
size = width, height = 600, 500
screen = pygame.display.set_mode(size)
text_resp = TextBox(screen, 0, 0, 500, 50)


def func():
    print(1)
    map_params = {
        'apikey': API_KEY,
        "geocode": ''.join(text_resp.text),
        "lang": 'ru_RU',
        "format": "json"
    }
    print(map_params['geocode'])
    map_api_server = 'http://geocode-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"].split()
        map_file = make_static_maps_response(toponym_coodrinates, delta,
                                             map_sat_hyb, toponym_coodrinates)
        blit_amg(map_file)
    else:
        print("Ошибка выполнения запроса:")
        print(response)
        print("Http статус:", response.status_code, "(", response.reason, ")")


button = Button(screen, 500, 0, 100, 50, text='Искать', onClick=func)
blit_amg(map_file)


if __name__ == '__main__':
    pygame.display.flip()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if 0.2 <= delta:
                        delta -= 0.1
                        map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                        blit_amg(map_file)
                if event.key == pygame.K_PAGEDOWN:
                    if delta <= 20:
                        delta += 0.1
                        map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                        blit_amg(map_file)
                if event.key == pygame.K_UP:
                    someval[1] += delta * 2
                    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                    blit_amg(map_file)
                if event.key == pygame.K_DOWN:
                    someval[1] -= delta * 2
                    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                    blit_amg(map_file)
                if event.key == pygame.K_LEFT:
                    someval[0] -= delta * 2
                    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                    blit_amg(map_file)
                if event.key == pygame.K_RIGHT:
                    someval[0] += delta * 2
                    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                    blit_amg(map_file)
                if event.key == pygame.K_F1:
                    map_sat_hyb = 'map'
                    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                    blit_amg(map_file)
                if event.key == pygame.K_F2:
                    map_sat_hyb = 'sat'
                    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                    blit_amg(map_file)
                if event.key == pygame.K_F3:
                    map_sat_hyb = 'hybrid'  # я  хз как гибрид писать
                    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                    blit_amg(map_file)
        pygame_widgets.update(events)
        pygame.display.flip()
    pygame.quit()