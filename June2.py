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
        if "id" in i.__dict__ and i.id==id:i.confirmed=True
        if i.type=="player0":player1=i
        if i.type=="player2":player2=i



    if typ==b"br":
        m=Bar(*numpy.array([a,b]).astype(int))
        I.add_obj(m)
        m.id=id
        N.add_static_object(m)
        m.confirmed=True

    elif typ==b"p0":
        print(a,b)
        player1.location=numpy.array(a).astype(int)
        player1.speed=b[0]
        player1.rotation=b[1]
        player1.id=id

    elif typ==b"p2":
        print(a,b)
        player2.id=id
        if player2.location==numpy.array(a).astype(int) and player2.speed==b[0] and player2.rotation==b[1]:
            player2.confirmed=True
            print("that is true")

    else:
        print(id, typ, a, b)





if __name__ == '__main__':
    pygame.display.set_caption("client")


    client=Client("127.0.0.1",("127.0.0.1",8081))
    client.handler=obj_handler

    player = N.add_controlled_object(Player([30, 50]))
    player.go_mask = I
    player.env = N
    player.local=False

    player2 = N.add_controlled_object(Player2([300, 50]))
    player2.go_mask = I
    player2.env = N

    client(N.objlis)

    st=sleep_til()


    while N.running:
        N.update()
        N.runner()

        client(N.objlis)
        st()
    client.sync_flag=False



