import pygame
import random

WIDTH = 800
HEIGHT = 650
FPS = 10

CMINUS = 5
CRADIUS = 50
CTH = 1
CPOR = 26

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# здесь при вызове надо читать и отдавать сет точек с координатами ax, ay (сразу из них делаются Rect и задается color)
def getpoints():
    res = []
    p = {}
    ax = random.random() * WIDTH
    ay = random.random() * HEIGHT
    p['rect'] = pygame.Rect(ax, ay, 5, 5)
    p['color'] = (255, 0, 0)
    res.append(p)
    return res

import math

def find_mid(arr):
    mx = 0
    my = 0
    mck = 0
    for am in arr:
        mx = mx + am['rect'][0]
        my = my + am['rect'][1]
        mck = mck + 1
    if mck == 0:
        return 0,0
    return mx / mck, my / mck


def find_group(arr):
    ar_res = []
    for t in range(round(255/CMINUS)):
        newar = []
        for r in arr:
            if abs(r['color'][1] - t*CMINUS) < CPOR:
                newar.append(r)
        ar_res.extend(find_g(newar))
    return ar_res


def find_g(arr):
    ar = []

    midx, midy = find_mid(arr)
    newarr = []
    for am2 in arr:
        if math.hypot(am2['rect'][0] - midx, am2['rect'][1] - midy) < CRADIUS:
            newarr.append(am2)
    if len(newarr) > CTH:
        midx, midy = find_mid(newarr)
        if midx != 0 and midy != 0:
            r = {}
            r['circle'] = (midx,midy)
            r['color'] = (0,255,0)
            ar.append(r)
    return ar


points = []

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Screen")

clock = pygame.time.Clock()
# Цикл
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    newpoints = []
    for pp in points:
        if pp['color'][1] < 255 - CMINUS:
            newc = (255, pp['color'][1] + CMINUS, pp['color'][2] + CMINUS)
            pp['color'] = newc
            newpoints.append(pp)
        #иначе она просто исчезает
    points = newpoints
    # Обновление
    p = getpoints()
    points.extend(p)

    cts = find_group(points)

    # Рендеринг
    screen.fill(WHITE)
    for pp in points:
        pygame.draw.rect(screen, pp['color'], pp['rect'], 0)
    for cc in cts:
        pygame.draw.circle(screen, cc['color'], cc['circle'], CRADIUS, 2)
    pygame.display.flip()

pygame.quit()
