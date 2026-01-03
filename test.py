from pygame import *
from random import randint

init()
window = display.set_mode((408, 300))
gold = image.load("lol.png")
# fourgold = Surface((24, 24))
# fourgold.blit(transform.flip(gold,True, False), (0, 0))
# fourgold.blit(gold, (12, 0))
# fourgold.blit(gold, (0, 12))
# fourgold.blit(transform.flip(gold,True, False), (12, 12))

forgoldmany = [surface.Surface((24, 24)) for _ in range(17)]
def randconfig():
    global forgoldmany
    for i in range(len(forgoldmany)):
        forgoldmany[i].blit(transform.flip(gold, randint(0,1), randint(0,1)), (0,0))
        forgoldmany[i].blit(transform.flip(gold, randint(0,1), randint(0,1)), (12,0))
        forgoldmany[i].blit(transform.flip(gold, randint(0,1), randint(0,1)), (0,12))
        forgoldmany[i].blit(transform.flip(gold, randint(0,1), randint(0,1)), (12,12))
CHANGE = USEREVENT + 1
time.set_timer(CHANGE, 500)
randconfig()
run = True
while run:
    window.fill((255, 255, 255))
    #window.blit(fourgold, (0, 0))
    for x in range(17):
        for i in range(len(forgoldmany)):
            window.blit(transform.flip(forgoldmany[i], x%2==0, x%4==0), (i * 24, x*24))
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == CHANGE:
            randconfig()
    display.update()
quit()