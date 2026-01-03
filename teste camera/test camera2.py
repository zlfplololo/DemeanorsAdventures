#!usr/bin/python3
from pygame import *

class Camera:
    def __init__(self, xonmap, yonmap):
        self.coords = {"x": xonmap, "y": yonmap}

    def __getitem__(self, key):
            return self.coords[key]
    
    def __setitem__(self, key, value):
            self.coords[key] = value

    def blitwith(self, Objx, Objy, Objimg):
        window.blit(Objimg, (Objx - self["x"], Objy - self["y"]))

init()
window = display.set_mode((500, 500))
background1 = Surface((500, 500))
background2 = Surface((250, 250))
inventory = transform.scale(image.load("itemframe.png"), (100, 100))
display.set_caption("Camera Test")
display.set_icon(inventory)
clock = time.Clock()
xpos, ypos = 0, 0
cam = Camera(-10, 0)

run = True
while run:
    window.fill((0,0,0))
    background1.fill((205, 205, 200))
    background2.blit(background1, (0,0))
    cam.blitwith(0,0, background2)
    for e in event.get():
        if e.type == QUIT:
            run = False

    keyc = key.get_pressed()
    if keyc[K_LEFT]:
        cam["x"] -= 5
    if keyc[K_RIGHT]:
        cam["x"] += 5
    if keyc[K_UP]:
        cam["y"] -= 5
    if keyc[K_DOWN]:
        cam["y"] += 5
    if keyc[K_a]:
        xpos -= 5
    if keyc[K_d]:
        xpos += 5
    if keyc[K_w]:
        ypos -= 5
    if keyc[K_s]:
        ypos += 5
    
    display.update()
    clock.tick(60)

quit()
