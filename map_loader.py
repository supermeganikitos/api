import json

import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import requests

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def make_static_maps_response(someval_, delta, map_or_sat):
    global someval, pt_s
    someval = list(map(float, someval_))
    delta = str(delta)
    map_params = {
        "ll": ",".join((str(someval_[0]), str(someval_[1]))),
        "spn": ",".join([delta, delta]),
        "l": map_or_sat
    }
    if pt_s:
        map_params['pt'] = '~'.join((','.join(i) for i in pt_s))
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def blit_amg(map_file):
    scr1 = pygame.image.load(map_file)
    screen.blit(scr1, (0, 50))


someval = [37.617698, 55.755864]
pt_s = []
delta = 0.2
map_sat_hyb = 'map'
map_file = make_static_maps_response(someval, delta, map_sat_hyb)
pygame.init()
pygame.display.set_caption('Карта')
size = width, height = 600, 550
screen = pygame.display.set_mode(size)
text_resp = TextBox(screen, 0, 0, 500, 50)
text_adress = TextBox(screen, 0, 500, 600, 50)


def func():
    map_params = {
        'apikey': API_KEY,
        "geocode": ''.join(text_resp.text),
        "lang": 'ru_RU',
        "format": "json"
    }
    map_api_server = 'http://geocode-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    if response:
        json_response = response.json()
        with open('js.json', 'w') as f:
            json.dump(json_response, f, indent=4)
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        adress = toponym['metaDataProperty']['GeocoderMetaData']["AddressDetails"]["Country"]["AddressLine"]
        text_adress.setText(adress)
        print(adress)
        toponym_coodrinates = toponym["Point"]["pos"].split()
        pt_s.append(toponym_coodrinates)
        map_file = make_static_maps_response(toponym_coodrinates, delta, map_sat_hyb)
        blit_amg(map_file)
    else:
        print("Ошибка выполнения запроса:")
        print(response)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def clear_func():
    pt_s.clear()
    text_adress.setText('')
    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
    blit_amg(map_file)


button_search = Button(screen, 500, 0, 50, 50, text='Искать', onClick=func, fontSize=15)
button_click = Button(screen, 550, 0, 50, 50, text='Очистить', onClick=clear_func, fontSize=15)
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
                        delta -= 0.05
                        map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                        blit_amg(map_file)
                if event.key == pygame.K_PAGEDOWN:
                    if delta <= 20:
                        delta += 0.05
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
                    map_sat_hyb = 'scl'  # я  хз как гибрид писать
                    map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                    blit_amg(map_file)
                if event.key == pygame.K_q:
                    clear_func()
        pygame_widgets.update(events)
        pygame.display.flip()
    pygame.quit()