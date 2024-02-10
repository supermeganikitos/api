import pygame
import requests

if __name__ == '__main__':
    try:
        someval = (float(input()), float(input()))
        delta = 0.02
        map_params = {
            "ll": ",".join((str(someval[0]), str(someval[1]))),
            "spn": delta,
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)
        map_file = "map.jpg"
        with open(map_file, "wb") as file:
            file.write(response.content)
        pygame.init()
        pygame.display.set_caption('Карта')
        size = width, height = 600, 450
        screen = pygame.display.set_mode(size)
        screen.blit(pygame.image.load(map_file), (0, 0))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
    except Exception as e:
        print('Unexcepted error: ' + e.__str__())