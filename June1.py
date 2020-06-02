from player.key import *

class Player2(Player):
    type="player2"
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

import time

from web_connection.main import *


def sleep_til():
    diff=0.015
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

#(cc),(ff),(ff)
#墙：p1,p2
#球：位，速
#人：位，[速,转]
def obj_handler(id,typ,a,b):
    for i in N.objlis:
        if "id" in i.__dict__ and i.id==id:
            i.confirmed=True
        if i.type=="player0":player1=i
        if i.type=="player2":player2=i

    if typ==b"p2":
        print(a,b)
        player2.location=numpy.array(a).astype(int)
        player2.speed=b[0]
        player2.rotation=b[1]
    else:
        print(id,typ,a,b)



if __name__ == '__main__':
    from maps.blitor import *

    server=Server(("127.0.0.1",8081),"127.0.0.1")
    server.handler=obj_handler


    # 随机生成些线，和小球方向
    N = Shower()
    pygame.display.set_caption("server")

    m = simple_map()
    N.add_static_objects(m)

    player = N.add_controlled_object(Player([30, 50]))
    player.go_mask = InMask(m)
    player.env = N

    player2 = N.add_controlled_object(Player2([300, 50]))
    player2.go_mask = InMask(m)
    player2.env = N
    player2.local=False

    server(N.objlis)

    st=sleep_til()



    last_pause = N.pause
    while N.running:
        if not N.pause:
            if last_pause is not N.pause:
                print(player.location)
        last_pause = N.pause
        N.update()
        N.runner()

        server(N.objlis)
        st()
    server.sync_flag=False