import numpy
from pygamenew.two_d_tanks.shower import *
import time

def ranges(x1,x2,x,range,partial=0):
    if partial:
        if x2==x1:return True
        return x2>=x>=x1 or x1>=x>=x2
    return x2>=x+range>=x1 or x1>=x+range>=x2 or x2>=x-range>=x1 or x1>=x-range>=x2

def collision(line,point,distance):
    (x1,y1),(x2,y2)=line
    #x/(x2-x1)*(y2-y1)-x1/(x2-x1)*(y2-y1)-y+y1=0
    #转到直线方程Ax+By+C=0
    x,y=point
    if ranges(x1,x2,x,distance):
        if ranges(y1,y2,y,distance):
            if not ranges(y1,y2,y,distance,1) or not ranges(x1,x2,x,distance,1):
                if numpy.linalg.norm(numpy.array(line[0])-point)>distance and numpy.linalg.norm(numpy.array(line[1])-point)>distance:return False

            try:
                C = y1 - x1 / (x2 - x1) * (y2 - y1)
                B = -1
                A = (y2 - y1) / (x2 - x1)

                x0, y0 = point
                # 点到直线的距离公式
                d = (A * x0 + B * y0 + C) / (A ** 2 + B ** 2) ** 0.5
            except:
                (y1, x1), (y2, x2) = line
                C = y1 - x1 / (x2 - x1) * (y2 - y1)
                B = -1
                A = (y2 - y1) / (x2 - x1)

                y0, x0 = point
                # 点到直线的距离公式
                d = (A * x0 + B * y0 + C) / (A ** 2 + B ** 2) ** 0.5

            print(d, distance, d <= distance)

            return d<=distance
    return False

def line_to_vector(line):
    (x1,y1),(x2,y2)=line
    return x2-x1,y2-y1


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

class Ball(Obj):
    def __init__(self,size,location,speed):
        #动画效果
        self.size=size
        self.location=numpy.array(location).astype("float64")
        #vector
        self.speed=numpy.array(speed)

    def __add__(self, other):
        print("使用了+")
        return self.碰撞箱(other)

    def 碰撞箱(self,obj):
        if type(obj)==dict:
            if "lines" in obj:
                lines=obj["lines"]
                for i in lines:
                    if collision(i,self.location,self.size):
                        self.碰撞(i)
        else:
            #默认是lines
            for i in obj:
                if collision(i, self.location, self.size):
                        self.碰撞(i)


    def 碰撞(self,obj):
        #默认是line
        """正交分解一个平行的向量，一个垂直的向量，垂直的向量取反，平行的不变"""
        p=line_to_vector(obj)
        # print(p)
        pline=numpy.dot(self.speed,p)/numpy.linalg.norm(p)
        # print(pline,p,p/numpy.linalg.norm(p))
        pline=p/numpy.linalg.norm(p)*pline
        # print(pline)
        cline=-pline+self.speed
        # print("cline:",end=" ")
        # print(cline)
        self.speed = pline-cline

    decay=100000

    color=[0,255,0]
    bgcolor=[255,255,255]

    @property
    def alive(self):
        return self.decay>0

    def upd(self,objs):
        self.decay-=1
        # print("upding")
        for i in objs:
            if "lines" in i.__dict__:
                self.碰撞箱(i.lines)
        self.location+=self.speed

    @property
    def locat(self):return self.location

    @property
    def object(self):
        surf = pygame.Surface((self.size*2,self.size*2))
        self.Rplac=(self.size,self.size)
        surf.fill(self.color)
        surf.set_colorkey(self.bgcolor)
        return surf


if __name__ == '__main__':

    #随机生成些线，和小球方向
    N=Shower()
    N.add_dynamic_object(Ball(5,[30,50],[1,0.5]))
    # N.add_dynamic_object(Ball(5,[30,50],[1,0.7]))
    # N.add_static
    for i in range(10):
        c=i%2
        N.add_dynamic_object(start_bar(150,[10+i*50,100+c*50],0))
    N.add_dynamic_object(start_bar(1000, [100, 20], 1))
    N.add_dynamic_object(start_bar(1000, [100, 220], 1))
    while N.running:
        N.update()
        N.runner()
        time.sleep(0.01)

