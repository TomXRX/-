from June1 import *






from maps.blitor import *

N = Shower()


I=InMask()

#(cc),(ff),(ff)
#墙：p1,p2
#球：位，速
#人：位，[速,转]
def obj_handler(id,typ,a,b):
    for i in N.objlis:
        if i.id==id:i.confirmed=True



    if typ==b"br":
        m=Bar(a,b)
        I.add_obj(m)
        m.id=id
        N.add_static_object(m)
        m.confirmed=True

    elif typ==b"p2":
        p

    else:
        print(id, typ, a, b)





if __name__ == '__main__':
    client=Client("127.0.0.1",("127.0.0.1",8081))
    client.handler=obj_handler

    while N.running:
        N.update()
        N.runner()

        client(N.objlis)

    client.sync_flag=False



