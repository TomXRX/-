from web_connection.structs import *
import time,socket,threading
class Server:
    def __init__(self,target,host=None):

        nq = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        n = socket.gethostname()
        if host is None:
            print(socket.gethostbyname_ex(n))
            nq.bind((socket.gethostbyname_ex(n)[-1][-1], 8080))
            print(socket.gethostbyname_ex(n)[-1])
        elif type(host) is str:
            nq.bind((host,8080))
        else:nq.bind(host)
        print(host,target)
        if type(target) is str:
            nq.connect((target, 8080))
        else:nq.connect(target)
        nq.setblocking(False)
        self.nq=nq









        import threading
        threading.Thread(target=self.send_loop).start()
        threading.Thread(target=self.recv_loop).start()








    new=True
    sleep=0.005

    sync_flag=True
    send=b""
    def send_loop(self):
        while self.sync_flag:

            if self.new and self.send:
                try:
                    self.nq.send(self.send)
                    self.send=b""
                    self.new = False

                except Exception as e:
                    if e.args[0]==10054:print("!",end="")
                    print("send_error",end=":")
                    print(e,e.args)


            else:
                time.sleep(self.sleep)


    recv=b""
    def recv_loop(self):
        while self.sync_flag:
            if self.new:
                self.new=False
                try:
                    self.recv=self.nq.recv(8192)
                    self.upded=False
                except Exception as e:
                    if e.args[0]==10035:continue
                    if e.args[0]==10054:
                        print("!",end="")
                        continue
                    print("recv_error",end=":")
                    print(e,e.args)
            else:
                time.sleep(self.sleep)




    def spliter(self,buffer):
        id,buffer=spliter("H",buffer)
        typ,buffer=spliter("cc",buffer)
        locat,buffer=spliter("ff",buffer)
        speed,buffer=spliter("ff",buffer)
        return [id,typ,locat,speed],buffer


    def decode(self, buffer):
        decode=[]
        while buffer:
            data, buffer = self.spliter(buffer)
            decode.append(data)
        return decode


    def update_objs(self,data):
        if data:
            for i in data:
                id,typ,a,b=i
                type=b""
                for i in typ:type+=i
                self.handler(id,type,a,b)

    def handler(self,id,typ,a,b):
        print("should be changed")

    def sync_obj(self,obj):
        # self.send.append([obj,time.perf_counter()])
        typ=obj.type
        if typ=="bar":
            a=obj.locat
            b=obj.locat2
        elif typ[:5]=="player"[:5]:
            a=obj.locat
            b=[obj.speed,obj.rotation]
        else:
            a=obj.locat
            b=obj.speed

        typ=typ[:1]+typ[-1:]
        # typ=typ[:2]+typ[-2:]

        # print(typ,a,b)

        if not "id" in obj.__dict__:
            obj.id=self.ids
            self.ids+=2
        self.send+=struct.pack("Hccffff",obj.id,*[i.encode() for i in typ],*a,*b)

    ids=0

    def __del__(self):
        self.sync_flag=False

    def need_sync(self,obj):
        # if not "_name" in obj.__dict__:return False
        if "confirmed" in obj.__dict__:return not obj.confirmed
        #TODO:玩家需要始终更新
        #TODO:子弹只需要更新一次
        return True

    upded=True
    def __call__(self, objs):
        if not self.upded:
            self.update_objs(self.decode(self.recv))
            self.upded=True

        self.send=b""
        for i in objs:
            if self.need_sync(i):
                self.sync_obj(i)


        self.new=True


class Client(Server):
    ids=1