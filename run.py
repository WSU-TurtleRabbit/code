#! /usr/bin/env python3
from WSUSSL.Networking.ServerClass import Server
from WSUSSL.World.model import Model as wm
from WSUSSL.World.receiver import proto2_ssl_vision_py_receiver as receiver
from WSUSSL.Shared.utils import main as UI

if __name__ ==  '__main__':
    # call world.model wm
    world_model = wm()
    world_receiver = receiver()
    # connect to other script (sending wm)
    world_receiver.set_world_model(world_model)
    world_receiver.listen()
    
    #server = Server(6)
    #server.send_action(UI())
