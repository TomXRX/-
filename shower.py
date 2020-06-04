import pygame
from pygame.locals import *

import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

class Obj():
    show = True
    alive=True
    name=""
    inited = 0
    got = 0
    Rplac=[0,0]
    def __init__(self, backgroundColor=[0, 0, 0], rector=[], locat=[0, 0], color=[0, 255, 0], name="", speedx=[], way=0,
                 **dic):
        self.BaseColor = (0, 0, 0)
        self.baseline = [[0, 0], [0, 0]]
        self.name = name
        assert len(locat) == 2
        self.locat = locat
        self.color = color
        assert len(rector) == 2
        self.rec = rector
        self.object = 0
        self.bgcolor = backgroundColor
        self.way = way
        self.Toprint = self.printees()
        for k in dic:
            self.__dict__[k] = dic[k]

    class printees():
        rect = []
        Rplac = []
        locat = []

        def __init__(self, color=[], rect=[], locat=[], ):
            pass

    def __sub__(self, other):
        return [self.locat[k] - other[k] for k in range(2)]

    def upd(self,obj):
        print("shall be changed")


class Shower:
    pressed = []
    printe = []

    def __init__(self, 宽=500, 高=500, backgroundColor=[255,255,255], headless=False):
        self.宽, self.高 = 宽, 高
        if not headless: self.init()
        self.headless = headless
        self.running = True
        self.objlis = []
        self.backgroundColor = backgroundColor
        self.font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 17)
        self.keys = pygame.key
        self.mouse = pygame.mouse

    def init(self, title="Toms'"):
        pygame.init()
        self.screen = pygame.display.set_mode((self.宽, self.高))
        pygame.display.set_caption(title)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):pass

    def set_headless(self, headless):
        if self.headless == headless: return None
        if self.headless:
            self.init()
        else:
            self.close()
        self.headless = headless

    def close(self):
        pygame.display.quit()

    def surfPrint(self, got):
        text_surface = self.font.render(str(got), True, (0, 0, 255))
        self.printe.append(text_surface)


    def add_dynamic_object(self,obj):
        obj.static=False
        self.objlis.append(obj)
        return obj


    def add_controlled_object(self,obj):
        obj.static=False
        obj.controlled=True
        self.objlis.append(obj)
        return obj


    def add_static_object(self,obj):
        obj.static=True
        self.objlis.append(obj)

    def add_static_objects(self,objs):
        for i in objs:self.add_static_object(i)

    def get_objects_by_name(self, name):
        get = []
        for n in self.objlis:
            if n.name == name:
                get.append(n)
        return get

    def get_objects_by_index(self, index):
        get = []
        for n in self.objlis:
            if "index" not in n.__dict__: continue
            if n.index == index:
                get.append(n)
        return get

    def get_object_by_index(self, index):
        try:
            return self.get_objects_by_index(index)[0]
        except:
            return None

    # @timethis
    def update(self,):
        if self.pause:return
        self.pressed = pygame.key.get_pressed()
        if self.pressed[K_ESCAPE]: self.running = 0
        for k in self.objlis:
            if "controlled" in k.__dict__:
                k.upd([i for i in self.objlis if i is not k],self.pressed)
            else:
                k.upd(i for i in self.objlis if i is not k)
            if not k.alive:
                self.objlis.remove(k)

    clear_print = True

    on_static=False
    static_surface=None

    # @timethis
    def bliter(self):
        if [(i.object,i-i.Rplac) for i in self.objlis if i.show and i.static ]:
            if not self.on_static:
                self.screen.fill(self.backgroundColor)
                self.screen.blits([(i.object, i - i.Rplac) for i in self.objlis if i.show and i.static])
                pygame.display.update()
                pygame.image.save(self.screen, "map.png")
                self.static_surface=pygame.image.load("map.png")
                self.on_static=True
            else:self.screen.blit(self.static_surface,(0,0))
        else:self.screen.fill(self.backgroundColor)


        self.screen.blits([(i.object,i-i.Rplac) for i in self.objlis if i.show and not i.static])
        i = 0
        for n in self.printe:
            self.screen.blit(n, (10, 20 + i * 30))
            i += 1
        self.drawer()
        if not self.headless: pygame.display.update()
        if self.clear_print: self.printe = []

    events = []

    def drawer(self):
        pass

    pause=False
    def runner(self, blit=True):
        # self.pressed=pygame.key.get_pressed()

        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.running = False
                elif event.key==K_BACKQUOTE:
                    if self.pause:print("paused")
                    self.pause = not self.pause
            elif event.type == QUIT:
                self.running = False
        if self.running:
            if blit: self.bliter()
        else:
            pygame.display.quit()

def sleep_til(diff=0.03):
    import time
    last_call=0
    first_call=True
    def call():
        nonlocal last_call,first_call
        interval=last_call-time.perf_counter()
        # print(interval,)
        if interval<0:
            if not first_call:print("too slow, time exceeded {} second for {} second interval".format(-interval,diff))
            else:first_call=False
            last_call=time.perf_counter()
        else:
            time.sleep(interval)
        last_call+=diff

    return call

