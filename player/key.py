from dynamic.ball import *
import math
class Player(Ball):
    type="player0"
    def __init__(self,location,size=10):
        self.size = size
        self.location = numpy.array(location).astype("float64")
        # self.control_keys=[[K_a,K_d],[K_w,K_s],K_m]
        self.control_keys=[[K_s,K_f],[K_e,K_d],K_q]

        self.bullet_name_space=[str(self.__hash__())+"bullet_{}".format(i) for i in range(5)]

    rotation=0
    speed = 0
    last_shoot=0
    env=None
    bullet_decay=1000
    max_speed=0.75
    local=True
    def upd(self, objs, keys):
        if self.local:

            a, d = self.control_keys[0]
            self.rotation -= (keys[a] - keys[d]) * 2

            self.tosp = 0
            w, s = self.control_keys[1]
            if keys[w]:
                if self.speed > -self.max_speed:
                    self.speed -= 0.1
                self.tosp = True
            if keys[s]:
                if self.speed < self.max_speed:
                    self.speed += 0.1
                self.tosp = True
            if not self.tosp:
                if self.speed > 0:
                    self.speed -= 0.1
                elif self.speed < 0:
                    self.speed += 0.1
                if -0.1 < self.speed < 0.1: self.speed = 0

        location=self.sim_next()

        # print(self.check_go(location),location)
        if not self.check_go(location):
            self.location=location

        #小动作，移动时
        if self.check_go(self.location):
            print("c",end="")
            gos=[[0,1],[1,0],[-1,0],[0,-1]]
            for i in gos:
                if not self.check_go(self.location+i):
                    self.location+=i
                    return

        if self.env is None:
            print("error")
            return


        bullets=self.bullet_name_space.copy()

        #发射子弹
        bu=[]
        last_decay=0
        for i in objs:
            if "_name" in i.__dict__:
                bu.append(i)
                for ii in bullets:
                    if i._name==ii:
                        bullets.remove(ii)
                        last_decay=max(i.decay,last_decay)
                        break
        if self.local:
            if self.last_shoot != keys[self.control_keys[-1]] and not self.last_shoot:
                if bullets and last_decay<self.bullet_decay-30:
                    # print("shoot")
                    # print(self.speed,self.size)
                    bullet = self.env.add_dynamic_object(Ball(3,
                                                              self.sim_next(self.size * 2.2 - self.speed * 3, speed=-1),
                                                              [-math.sin(-self.rotation / 180 * math.pi),
                                                               -math.cos(-self.rotation / 180 * math.pi)]))
                    bullet._name = bullets[0]
                    bullet.decay = self.bullet_decay
            self.last_shoot = keys[self.control_keys[-1]]

        bullets=bu
        masks=[]
        placs=[]
        #接收子弹
        for i in bullets:
            masks.append(pygame.mask.from_surface(i.object))
            placs.append(i.locat)
        mask = pygame.mask.from_surface(self.object)
        # collision=None
        for m, p, b in zip(masks, placs,bullets):
            # print(".",end="")
            plac=numpy.array(self.location)-numpy.array(self.Rplac)
            get=p-plac
            collision = mask.overlap(m, get.astype(int))
            if b.decay>self.bullet_decay-15:pass
            elif collision:
                b.decay=0
                self.alive=False
                # return collision
    alive = True

    def sim_next(self, literation=1,speed=None):
        if speed is None:speed=self.speed
        location=numpy.array([0,0]).astype("float64")
        location[0]=self.location[0] + math.sin(-self.rotation/180 * math.pi) * speed*literation
        location[1]=self.location[1] + math.cos(-self.rotation/180 * math.pi) * speed*literation
        return location

    go_mask=None
    def check_go(self,location):
        if self.go_mask is None:
            print("error")
            return
        return self.go_mask(self.object,(location-self.Rplac).astype("int"))

    @property
    def object(self):
        def init():

            try:surf=pygame.image.load(r"..\img\tank22.png").convert_alpha()
            except:surf=pygame.image.load(r"img\tank22.png").convert_alpha()
            # surf = pygame.Surface((self.size*2,self.size*2))
            # surf.fill(self.color)
            # surf.set_colorkey(self.bgcolor)
            return surf

        if not self.inited:
            self.surf = init()
            self.inited = 1
        a = pygame.transform.rotate(self.surf, -self.rotation)
        rec = [0, 0]
        rec[0] = a.get_size()[0] / 2
        rec[1] = a.get_size()[1] / 2
        self.Rplac=rec
        return a



if __name__ == '__main__':
    from maps.blitor import *
    #随机生成些线，和小球方向
    N=Shower()
    m=simple_map()
    N.add_static_objects(m)

    player=N.add_controlled_object(Player([30,50]))
    player.go_mask=InMask(m)
    player.env=N

    last_pause=N.pause
    while N.running:
        if not N.pause:
            if last_pause is not N.pause:
                print(player.location)
        last_pause=N.pause
        N.update()
        N.runner()



        time.sleep(0.01)