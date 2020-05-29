import pygame,numpy
from pygamenew.two_d_tanks.shower import *




class Bar(Obj):
    color = [0, 0, 0]
    bgcolor = [255, 255, 255]

    def __init__(self, p1, p2):
        print(p1,p2)
        (x1,y1),(x2,y2)=p1,p2
        self.lines = [[[x1,y1],[x2,y1]],[[x2,y1],[x2,y2]],[[x2,y2],[x1,y2]],[[x1,y2],[x1,y1]]]
        self.locat = p1
        p2 = numpy.array(p2)
        surf = pygame.Surface((p2 - p1))
        surf.fill(self.color)
        surf.set_colorkey(self.bgcolor)
        self.object = surf

    def upd(self, obj):
        pass

def start_bar(lenth,center,vertical,size=10):
    if vertical:return Bar((center[0]-lenth//2,center[1]-size//2),(center[0]+lenth//2,center[1]+size//2))
    return Bar((center[0] - size // 2, center[1] - lenth // 2),(center[0] + size // 2, center[1] + lenth // 2))

def simple_map(distance=100,mount=4):
    lis=[]
    for i in range(mount):
        c = i % 2
        lis.append(start_bar(150, [10 + i * distance + 50, 100 + c * distance], 0))
    lis.append(start_bar(200, [10, 120], 0))
    lis.append(start_bar(200, [460, 120], 0))
    lis.append(start_bar(1000, [100, 20], 1))
    lis.append(start_bar(1000, [100, 220], 1))
    return lis








if __name__ == '__main__':
    with Shower() as s:
        while 1:
            s.runner()
