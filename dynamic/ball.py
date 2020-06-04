import numpy
from shower import *
from maps.blitor import *
import time

def ranges(x1,x2,x,range,partial=0):
    if x2 == x1:
        if x+range>=x1>=x-range:
            return True

    if partial:
        return x2>=x>=x1 or x1>=x>=x2

    return x2>=x+range>=x1 or x1>=x+range>=x2 or x2>=x-range>=x1 or x1>=x-range>=x2

def collision(line,point,distance,strict=False):
    (x1,y1),(x2,y2)=line
    #x/(x2-x1)*(y2-y1)-x1/(x2-x1)*(y2-y1)-y+y1=0
    #转到直线方程Ax+By+C=0
    x,y=point

    if ranges(x1,x2,x,distance) and ranges(y1,y2,y,distance):
        # print(line, point, distance)
        # print("!.",end="")
        if not ranges(y1, y2, y, distance, 1) or not ranges(x1, x2, x, distance, 1):
            # print(".!", end="")
            if numpy.linalg.norm(numpy.array(line[0]) - point) > distance and numpy.linalg.norm(
                numpy.array(line[1]) - point) > distance: return False
            if strict:return False
            # print("point collision")
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

        # print(d, distance, abs(d) <= distance)
        # TODO:返回数字以用于排序
        return abs(d) <= distance

    return False

def line_to_vector(line):
    (x1,y1),(x2,y2)=line
    return x2-x1,y2-y1

class Ball(Obj):
    type="ball"
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
                self.碰撞箱(lines)
        else:
            #默认是lines

            c_objs=[]
            for i in obj:
                #TODO:？？？
                if collision(i, self.location, self.size,True) and collision(i, self.sim_next(2), self.size,True)\
                        and not collision(i, self.sim_last(), self.size,True):
                            c_objs.append(i)
            if c_objs:
                # print(c_objs,self.location,self.sim_next())
                for i in c_objs:self.碰撞(i)
                return
            for i in obj:
                if collision(i, self.location, self.size) and collision(i, self.sim_next(), self.size)\
                        and not collision(i, self.sim_last(), self.size):
                    c_objs.append(i)
            if len(c_objs)==1:
                self.碰撞(c_objs[0])
                print(c_objs[0],self.location,end="")
                print("??")
            # elif len(c_objs):
            #     print("many_collision")
            #     print(len(c_objs))

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

    decay=10000

    color=[0,255,0]
    bgcolor=[255,255,255]

    @property
    def alive(self):
        return self.decay>0

    def upd(self,objs,keys=None):
        self.decay-=1
        # print("upding")
        for i in objs:
            if "lines" in i.__dict__:
                self.碰撞箱(i.lines)
        self.location+=self.speed

    def sim_next(self, literation=1):
        return self.location + self.speed * literation

    def sim_last(self,literation=1):
        return self.location-self.speed*literation

    @property
    def locat(self):return self.location


    changed=0
    @property
    def object(self):
        def init():
            try:surf=pygame.image.load(r"..\img\ball1.png").convert_alpha()
            except:surf=pygame.image.load(r"img\ball1.png").convert_alpha()
            # surf = pygame.Surface((self.size*2,self.size*2))
            # surf.fill(self.color)
            # surf.set_colorkey(self.bgcolor)
            return surf

        if not self.inited:
            self.surf = init()
            self.inited = 1

        self.Rplac=(self.size,self.size)
        return self.surf

class MaskBall(Ball):
    def 碰撞箱(self,obj):
        # x=time.perf_counter()
        # print(x)
        mask = pygame.mask.from_surface(self.object)
        obj_mask=pygame.mask.from_surface(obj.object)
        obj_plac=obj.locat

        plac = numpy.array(self.location) - numpy.array(self.Rplac)
        get = obj_plac - plac
        collision = mask.overlap(obj_mask, get.astype(int))
        #?? collision=numpy.linalg.norm(get)<=self.size
        # print(x-time.perf_counter())
        return collision

    # @timethis
    def upd(self,objs,keys=None):
        
        self.decay-=1
        # print("upding")
        for i in objs:
            if "lines" in i.__dict__:
                if self.碰撞箱(i):
                    super().碰撞箱(i.lines)
                    
        self.location+=self.speed

Ball=MaskBall
if __name__ == '__main__':
    from maps.blitor import *
    #随机生成些线，和小球方向
    N=Shower()
    ball=N.add_dynamic_object(Ball(5,[159.5 , 108.65], [0.5 , 0.85]))
    # N.add_static
    N.add_static_objects(simple_map())

    N.pause=True
    last_pause=N.pause
    while N.running:
        if not N.pause:
            if last_pause is not N.pause:
                print(ball.location,ball.speed)
        last_pause=N.pause
        N.update()
        N.runner()
        time.sleep(0.01)

