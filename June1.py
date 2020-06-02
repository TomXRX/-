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

import time,socket,threading


class Server:
    def __init__(self,target,host=None):

        nq = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        n = socket.gethostname()
        if host==None:
            print(socket.gethostbyname_ex(n))
            nq.bind((socket.gethostbyname_ex(n)[-1][-1], 8080))
            print(socket.gethostbyname_ex(n)[-1])
        elif type(host) is str:
            nq.bind((host,8080))
        else:nq.bind(host)
        nq.connect((target, 8080))
        nq.setblocking(False)
        self.nq=nq

        import threading
        threading.Thread(target=self.send_loop).start()
        threading.Thread(target=self.recv_loop).start()

    new=True
    sleep=0.005

    sync_flag=True
    send=[]
    def send_loop(self):
        while self.sync_flag:

            if self.new:
                self.new=False
                for i in self.send:
                    self.nq.send(i)

            else:
                time.sleep(self.sleep)
    recv=[]
    def recv_loop(self):
        while self.sync_flag:
            if self.new:
                self.new=False
                try:
                    self.nq.recv(1024)
                except Exception as e:
                    if e.args[0]==10035:continue
                    print(e,e.args)
            else:
                time.sleep(self.sleep)


    def sync_obj(self,obj):
        self.send.append([obj,time.perf_counter()])

    def __del__(self):
        self.sync_flag=False

    def need_sync(self,obj):
        if not "_name" in obj.__dict__:return False
        #TODO:子弹只需要更新一次
        return True


    def __call__(self, objs):

        for i in objs:
            if self.need_sync(i):
                self.sync_obj(i)



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


if __name__ == '__main__':
    from maps.blitor import *

    server=Server("127.0.0.1")

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