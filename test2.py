from pygame import *
from random import randint

def pallete_swap(surf, old_c, new_c):
    nsurf = surf.copy()
    nsurf.fill(new_c)
    surf.set_colorkey(old_c)
    nsurf.blit(surf, (0, 0))
    surf.blit(nsurf, (0, 0))
    return nsurf

def pallete_swap_multiple(surf, *args):
    nsurf = surf.copy()
    for i in range(0, len(args)):
        nsurf = pallete_swap(nsurf, args[i][0], args[i][1])
    return nsurf
def palette_swap_list(surf, lst):
    nsurf = surf.copy()
    for i in range(0, len(lst)):
        nsurf = pallete_swap(nsurf, lst[i][0], lst[i][1])
    return nsurf

def mask_from(surf):
    nsurf = surf.copy()
    nsurf.fill((0, 0, 0))
    for i in range(surf.get_width()):
        for j in range(surf.get_height()):
            r, g, b, a = surf.get_at((i, j))
            if a != 0:
                nsurf.set_at((i, j), (255, 255, 255, 255))
            else:
                nsurf.set_at((i, j), (0, 0, 0, 0))
    return nsurf

def multiply_color(surf, color):
    nsurf = surf.copy()
    for i in range(surf.get_width()):
        for j in range(surf.get_height()):
            r, g, b, a = surf.get_at((i, j))
            r = (r * color[0]) // 255
            g = (g * color[1]) // 255
            b = (b * color[2]) // 255
            nsurf.set_at((i, j), (r, g, b, a))
    return nsurf
def mask_multiply(surf, mask):
    nsurf = surf.copy()
    for i in range(surf.get_width()):
        for j in range(surf.get_height()):
            r1, g1, b1, a1 = surf.get_at((i, j))
            r2, g2, b2, a2 = mask.get_at((i, j))
            r = (r1 * r2) // 255
            g = (g1 * g2) // 255
            b = (b1 * b2) // 255
            nsurf.set_at((i, j), (r, g, b, a2))
    return nsurf

init()
window = display.set_mode((500, 500))
tools = transform.scale(image.load("animations/Sword.png"), (404, 164))
atools = mask_from(tools)
gold = [((255, 0, 0), (251, 226, 54)), ((255, 0, 255), (251, 226, 54)), ((0, 0, 255), (251, 226, 54)), ((255, 255, 0), (255, 249, 125)), ((0, 255, 255), (255, 249, 125)), ((255, 255, 255), (255, 249, 125))]
tools = mask_multiply(palette_swap_list(tools, gold), atools)
fillin = transform.scale(image.load("SPT.png"), (250, 250))
fillin2 = transform.scale(image.load("Sprite-test.png"), (250, 250))
fillin2cp = pallete_swap_multiple(fillin2, ((0, 0, 0), (255, 0, 0)), ((255, 255, 255), (0, 0, 255)), ((126, 126, 126), (225, 0, 225)), ((63, 63, 63), (255, 0, 126)), ((189, 189, 189), (126, 0, 255)))
fillincp = multiply_color(fillin, (255, 255, 255))

CHANGE = USEREVENT + 1
time.set_timer(CHANGE, 500)
changee = True
run = True
while run:
    window.fill((106, 100, 106))
    window.blit(fillincp, (0, 0))
    window.blit(fillin2cp, (250, 0))
    window.blit(tools, (0, 250))
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == CHANGE:
            if changee:
                fillincp = multiply_color(fillin, (randint(100, 255), randint(100, 255), randint(100, 255)))
                fillin2cp = pallete_swap_multiple(fillin2, ((0, 0, 0), (randint(0, 255), randint(0, 255), randint(0, 255))), ((255, 255, 255), (randint(0, 255), randint(0, 255), randint(0, 255))), ((126, 126, 126), (randint(0, 255), randint(0, 255), randint(0, 255))), ((63, 63, 63), (randint(0, 255), randint(0, 255), randint(0, 255))), ((189, 189, 189), (randint(0, 255), randint(0, 255), randint(0, 255))))
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                changee = not changee    
    display.update()