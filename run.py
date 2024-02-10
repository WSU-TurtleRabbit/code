#! /usr/bin/env python3
from WSUSSL.Networking.ServerClass import Server
from WSUSSL.World.model import Model as wm
#from WSUSSL.World.receiver import proto2_ssl_vision_py_receiver as receiver
from WSUSSL.World.receiver import proto2_ssl_receiver as receiver
from WSUSSL.Shared.utils import main as UI
from WSUSSL.TeamControl.Skills.GoTowards import GoTowards as goto


if __name__ ==  '__main__':
    # call world.model wm
    world_model = wm()
    #world_receiver = receiver('',12345)
    #world_receiver = receiver()
    #world_receiver.set_world_model(world_model)

    #world_receiver.listen()

    server = Server(0)

    # connect to other script (sending wm)
    while True:
        #world_receiver.listen()
        robot_id = int(input("Enter Robot ID"))
        skill = goto(world_model,robot_id)
        skill.execute()
        server.send_action()
        # server.send_action(go_to_ball(world_model,6))
