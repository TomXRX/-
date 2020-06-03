from June1 import *






from maps.blitor import *

N = Shower()


I=InMask()

#(cc),(ff),(ff)
#墙：p1,p2
#球：位，速
#TODO:bullet decay field
#人：位，[速,转]

def obj_handler(id,typ,a,b):
    get=None
    player1=None
    player2=None
    for i in N.objlis:
        if "id" in i.__dict__ and i.id==id:
            i.confirmed=2
            get=i

        if i.type=="player0":player1=i
        if i.type=="player2":player2=i



    if typ==b"br":
        print(id,"br")
        if get is None:
            # m = Bar(*numpy.array([a, b]).astype(int))
            m = Bar((int(a[0]),int(a[1])),(int(b[0]),int(b[1])))
            I.add_obj(m)
            m.id = id
            N.add_static_object(m)
            m.confirmed = 2

    elif typ==b"p0":
        if player1 is None:return

        player1.location=numpy.array(a).astype(int)
        player1.speed=b[0]
        player1.rotation=b[1]
        player1.id=id

    elif typ==b"p2":
        #not using?
        if player2 is None:return
        player2.id=id
        if player2.location==numpy.array(a).astype(int) and player2.speed==b[0] and player2.rotation==b[1]:
            player2.confirmed=True
            print("that is true")
    elif typ==b"bl":
        if get is None:
            b=N.add_dynamic_object(Ball(3,numpy.array(a),numpy.array(b)))
            b.id=id
            b.confirmed=2
            b._name="other"
            b.decay=player1.bullet_decay



    else:
        print(id, typ, a, b)





if __name__ == '__main__':
    pygame.display.set_caption("client")


    # client=Client("127.0.0.1",("127.0.0.1",8081))
    client=Client("10.80.62.156")
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



