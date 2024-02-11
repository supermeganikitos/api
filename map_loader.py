import pygame
import requests


def make_static_maps_response(someval, delta, map_or_sat):
    delta = str(delta)
    map_params = {
        "ll": ",".join((str(someval[0]), str(someval[1]))),
        "spn": ",".join([delta, delta]),
        "l": map_or_sat
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def blit_amg(map_file):
    scr1 = pygame.image.load(map_file)
    screen.blit(scr1, (0, 0))


if __name__ == '__main__':
    try:
        someval = [float(input()), float(input())]
        delta = 0.2
        map_sat_hyb = 'map'
        map_file = make_static_maps_response(someval, delta, map_sat_hyb)
        pygame.init()
        pygame.display.set_caption('Карта')
        size = width, height = 600, 450
        screen = pygame.display.set_mode(size)
        blit_amg(map_file)
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
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
                    if event.key == pygame.K_1:
                        map_sat_hyb = 'map'
                        map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                        blit_amg(map_file)
                    if event.key == pygame.K_2:
                        map_sat_hyb = 'sat'
                        map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                        blit_amg(map_file)
                    if event.key == pygame.K_3:
                        map_sat_hyb = 'hybrid' # я  хз как гибрид писать
                        map_file = make_static_maps_response(someval, delta, map_sat_hyb)
                        blit_amg(map_file)
            pygame.display.flip()
        pygame.quit()
    except Exception as e:
        print('Unexcepted error: ' + e.__str__())