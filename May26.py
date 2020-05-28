import pygame
from pygame.locals import *
import math
import random
宽=1366
高=700
宽=int(宽/2)
# 宽=500
# 高=500
'''仅支持正方形和圆形'''
if True:
    def gougu(a, b):
        return (a ** 2 + b ** 2) ** 0.5
    def distance(a, b):
        return gougu(a[0] - b[0], a[1] - b[1])
    def surfaceholder():
        pass
    def bliter(a):
        return math.sin(player.rote * math.pi) * a[1] - math.cos(player.rote * math.pi) * a[0], math.cos(player.rote * math.pi) * a[1] + math.sin(player.rote * math.pi) * a[0]
    class Player(pygame.sprite.Sprite):
        def __init__(self, size=[10], height=10, color=(255, 0, 255)):
            self.surf = pygame.Surface((size[0], size[len(size) - 1]))
            self.rector=[0,0]
            self.rote = 0
            self.speed = [0, 0]
            self.size = size
            self.height = height
            self.color = color

        def mailuner(self):
            if self.rote != 0:
                a = pygame.transform.rotate(self.surf, self.rote)
                return a, a.get_size()
            else:
                return self.surf, self.size

        def updat(self, pressed_keys):
            self.tosp = [False, False]
            if True:
                if pressed_keys[K_r]:
                    self.rote=0
                if pressed_keys[K_e]:
                    self.rote += 0.01
                if pressed_keys[K_q]:
                    self.rote -= 0.01
                if pressed_keys[K_w]:
                    if self.speed[1] > -10:
                        self.speed[1] -= 0.5
                    self.tosp[1] = True
                if pressed_keys[K_s]:
                    if self.speed[1] < 10:
                        self.speed[1] += 0.5
                    self.tosp[1] = True
                if pressed_keys[K_a]:
                    if self.speed[0] > -10:
                        self.speed[0] -= 0.5
                    self.tosp[0] = True
                if pressed_keys[K_d]:
                    if self.speed[0] < 10:
                        self.speed[0] += 0.5
                    self.tosp[0] = True
            if not self.tosp[0]:
                if self.speed[0]>0:
                    self.speed[0]-=0.5
                elif self.speed[0]<0:
                    self.speed[0]+=0.5
            if not self.tosp[1]:
                if self.speed[1]>0:
                    self.speed[1]-=0.5
                elif self.speed[1]<0:
                    self.speed[1]+=0.5

            if pressed_keys[K_SPACE]:
                if self.speed[0] > 0:
                    self.speed[0] -= 0.1
                elif self.speed[0] < 0:
                    self.speed[0] += 0.1
                if self.speed[1] > 0:
                    self.speed[1] -= 0.1
                elif self.speed[1] < 0:
                    self.speed[1] += 0.1
            self.rector[0]+=math.sin(self.rote*math.pi)*self.speed[1]-math.cos(self.rote*math.pi)*self.speed[0]
            self.rector[1]+=math.cos(self.rote*math.pi)*self.speed[1]+math.sin(self.rote*math.pi)*self.speed[0]

        def __sub__(self, other):
            return (self.rector[0] - other.rector[0], self.rector[1] - other.rector[1])

        def rela(self, other):
            f = (type(other) == tuple)
            if not f:
                a, b = other - self
            else:
                a = other[0] - self.rect[0]
                b = other[1] - self.rect[1]
            if b == 0:
                f = 1 / 2 * math.pi
            else:
                f = math.atan(a / b)
            if a == 0: f = 0
            if a < 0:
                f += math.pi
                if b > 0: f += math.pi
            elif b < 0:
                f += math.pi
            return f

        def __eq__(self, other):
            if len(self.size) == 1 & len(other.size) == 1:
                return distance(self.rector, other.rector) <= self.size[0] + other.size[0]

    class Thing(Player):
        def __init__(self, loc, size=[100], height=10, color=(255, 255, 255)):
            super(Thing, self).__init__(size, height, color)
            self.rector[0]+=loc[0]
            self.rector[1]+=loc[1]
            if len(size)-1:
                self.points=[point(loc,i,size,height) for i in range(4)]

        def updat(self):
            self.rector[0]+=self.speed[0]
            self.rector[1]+=self.speed[1]
    class point():
        def __init__(self,loc,num, size=[100], height=10, color=(255, 255, 255),rote=0,):
            self.loc=loc
            self.num=num
            self.size=size
            self.height=height
            self.color=color
            self.updat(rote)
        def updat(self,rote):
            num=self.num
            # if self.num==2:num=3
            # if self.num==3:num=2

            #可能出错
            self.rector = self.loc[0] +math.cos(rote * math.pi) * self.size[0]/2 * (-1) ** int(num / 2) + math.sin(
                rote * math.pi) * self.size[1]/2 * (-1) ** num,self.loc[1] - math.sin(rote * math.pi) * self.size[0]/2 * (-1) ** int(num / 2) + math.cos(
                rote * math.pi) * self.size[1]/2 * (-1) ** num


    pygame.init()
    player = Player()
    Things = []
    for f in range(50):
        Things.append(Thing((random.randint(-1000,1000),random.randint(-1000,1000)),[random.randint(10,100),random.randint(
            10,100)],random.randint(0,100),(random.randint(0,255),random.randint(0,255),random.randint(0,255))))
    # for f in range(50):
    #     Things.append(Thing((random.randint(-1000,1000),random.randint(-1000,1000)),[random.randint(10,100)]))

    Things.append(Thing((0, 0), [100, 100], 10, (0, 255, 255)))
    Things.append(Thing((0, 0), [50], 5, (0, 0, 255)))
    ThU=[]
    for U in Things:
        ThU.append(0)

    screen = pygame.display.set_mode((宽*2, 高))
    # screen = pygame.display.set_mode((宽, 高))
    running = True
    font = pygame.font.SysFont("宋体", 50)
    qq = 0
    # oldposition=[0,0,0,0,0,0]
    # oldpN=0
blink=0
while running:
    pressed_keys = pygame.key.get_pressed()
    # P=False
    # for a in pressed_keys:
    #     if a:
    #         P=True
    #         break
    # if not P:
    #     if pygame.event.wait():
    #         continue

    if True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: running = False
            elif event.type == QUIT:
                running = False
        screen.fill([0, 255, 0])
        text_surface = font.render("location"+ str([int(player.rector[0]),int(player.rector[1])])+str(player.rote), True, (0, 0, 255))
        player.updat(pressed_keys)
    # screen.blit(a, (player.rect.x - w / 2, player.rect.y - h / 2))
    TU=0
    for T in Things:
        # a,b=T.mailuner()
        # w,h=b
        # screen.blit(a, ((T-player)[0]-w/2+宽/2,(T-player)[1]+高/2-h/2))
        x,y=bliter(T-player)
        if y>0&(-100<x<100):
            ThU[TU]=0
        else:ThU[TU]=1
        if len(T.size)-1:
            surf = pygame.Surface((T.size[0], T.size[1]))
            surf.fill(T.color)
            surf.set_colorkey((255, 0, 0))
            a = pygame.transform.rotate(surf, player.rote*180)
            rec = [0, 0]
            rec[0] -= a.get_size()[0] / 2
            rec[1] -= a.get_size()[1] / 2
            rec[0] += x+ 宽 / 2
            rec[1] += y+ 高 / 2
            # pygame.draw.rect(screen,T.color,Rect(int(x -T.size[0]/2+ 宽 / 2), int(y -T.size[1]/2+ 高 / 2),  T.size[0],  T.size[1]))
            screen.blit(a, rec)
            # pygame.draw.rect(screen,T.color, T.surf)
        else:
            pygame.draw.circle(screen, T.color, (int(x + 宽 / 2), int(y + 高 / 2)), T.size[0])
        # T.updat()
        k=player==T
        if k:
            screen.blit(font.render(str(k), True, (0, 0, 255)), (500, 20))
            # for kj in k[1:]:
                # pygame.draw.rect(screen,(255,255,0),(int(kj[0]) + 宽 / 2-player.rect[0],int(kj[1]) + 高 / 2-player.rect[1],10,10))
                # if not abs(kj[2])>=100:
                #     pygame.draw.line(screen,(255,100,0),(int(kj[0]) + 宽 / 2-player.rect[0],int(kj[1]) + 高 / 2-player.rect[1]),(100+ 宽 / 2-player.rect[0],int(kj[1]+(100-kj[0])*(-kj[2])) + 高 / 2-player.rect[1]))
        TU+=1
    # q=player == Tsssa
    # if not q==qq:
    #     qq=q
    #     print(q)
    pygame.draw.circle(screen,player.color,(int(宽/2), int(高/ 2)),player.size[0])
    # screen.blit(a, (宽/2- w / 2, 高/ 2- h / 2))
    screen.blit(text_surface, (10, 20))
    pygame.draw.line(screen,(0,0,0),(int(宽/2)-1,0),(int(宽/2)-1,高),2)
    screen.fill([0,0,0],Rect(宽, 0, 宽, 高))


    TU = -1
    time_passed = pygame.time.Clock().tick(400)
    time_passed_second = time_passed / 1000.0
    # blink+=1
    pygame.display.update()