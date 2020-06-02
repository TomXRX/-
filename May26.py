from player.key import *

class Player2(Player):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.control_keys=[[K_a,K_d],[K_w,K_s],K_m]
        self.control_keys=[[K_LEFT,K_RIGHT],[K_UP,K_DOWN],K_SLASH]


    @property
    def object(self):
        def init():

            try:surf=pygame.image.load(r"..\img\tank21.png").convert_alpha()
            except:surf=pygame.image.load(r"img\tank21.png").convert_alpha()
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

    # 随机生成些线，和小球方向
    N = Shower()
    m = simple_map()
    N.add_static_objects(m)

    player = N.add_controlled_object(Player([30, 50]))
    player.go_mask = InMask(m)
    player.env = N

    player2 = N.add_controlled_object(Player2([300, 50]))
    player2.go_mask = InMask(m)
    player2.env = N

    last_pause = N.pause
    while N.running:
        if not N.pause:
            if last_pause is not N.pause:
                print(player.location)
        last_pause = N.pause
        N.update()
        N.runner()

        time.sleep(0.005)