import pygame,numpy,time
from shower import *




class Bar(Obj):
    type="bar"
    color = [0, 0, 0]
    bgcolor = [255, 255, 255]

    def __init__(self, p1, p2):
        print(p1,p2)
        (x1,y1),(x2,y2)=p1,p2
        self.lines = [[[x1,y1],[x2,y1]],[[x2,y1],[x2,y2]],[[x2,y2],[x1,y2]],[[x1,y2],[x1,y1]]]
        self.locat = p1
        self.locat2=p2
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

def a_bar():
    return [start_bar(100,[150,150],0)]

class InMask():
    masks=[]
    placs=[]
    def __init__(self,objs=()):
        for i in objs:
            self.add_obj(i)

    def add_obj(self,i):
        self.masks.append(pygame.mask.from_surface(i.object))
        self.placs.append(i.locat)

    def __call__(self, obj,plac,):
        mask=pygame.mask.from_surface(obj)
        # collision=None
        for m,p in zip(self.masks,self.placs):

            collision=mask.overlap(m,-plac+p)
            if collision:return collision
        return None


if __name__ == '__main__':
    N = Shower()
    m=simple_map()
    # m=a_bar()
    N.add_static_objects(m)
    mask=InMask(m)

    bluesquare = pygame.Surface((20, 20)).convert_alpha()
    bluesquare.fill((10, 10, 255))
    bluesquare_rect = bluesquare.get_rect(topleft=(0, 0))  # 定位
    bluemask = pygame.mask.from_surface(bluesquare)

    last_pause = N.pause
    while N.running:
        last_pause = N.pause
        N.update()
        N.runner()


        x2, y2 = pygame.mouse.get_pos()
        bluesquare_rect.topleft=(x2,y2)
        p = mask(bluesquare,numpy.array([x2,y2]))
        N.screen.blit(bluesquare,bluesquare_rect)
        pygame.display.update()
        if p:
            碰撞点 = bluesquare_rect.x + p[0], bluesquare_rect.y + p[1]
            info = "offset=" + str(p) + ",p=" + str(p) + ",碰撞点坐标:" + str(碰撞点)
            pygame.display.set_caption(info)
        else:
            pygame.display.set_caption("无碰撞")

        time.sleep(0.1)



        time.sleep(0.01)
