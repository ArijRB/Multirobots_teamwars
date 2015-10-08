from game0 import *
from time import sleep


def dt(): td();td()


def gotox(_x):
    # le perso doit etre dirige vers le Nord
    global x
    tg()
    while _x < x:
        av()
        x-=1
    dt()
    while _x > x:
        av()
        x+=1
    tg()

def gotoy(_y):
    # le perso doit etre dirige vers le Nord
    global y
    while _y > y:
        av()
        y+=1
    dt()
    while _y < y:
        av()
        y-=1
    dt()

def goto(_x,_y):
    # le perso doit etre dirige vers le Nord
    global x,y
    if _x > x and _y >= y:
        gotox(_x);gotoy(_y)
    if _x > x and _y < y:
        gotox(_x);gotoy(_y)
    if _x < x and _y <= y:
        gotoy(_y);gotox(_x)
    if _x < x and _y > y:
        gotoy(_y);gotox(_x)


def main():
    global x,y
    init('tiny_complete')
    avk(8)

    #j = game.player
    #j.forward(j.rect.width)
    #coll_boxes = game.mask.get_box_collision_list( game.layers['personnage'], j)
    #j.resume_to_backup()
    #print coll_boxes

    sleep(1)
    l = parle('bonjour Roi')
    td()
    x = 1 ; y = 0
    sleep(0.2)

    for i,j,n in l:
        goto(i+1,j-1)
        sleep(0.2)
        goto(i,j-1)
        parle('bonjour '+n)
        ra()
        sleep(0.2)
        goto(i+1,j-1)
        sleep(0.2)
        goto(1,0)

    av()
    for i in range(4):
        tg();dp();av();dp();av()
    av()

if __name__ == '__main__':
    main()