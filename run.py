#! /usr/bin/env python3
from WSUSSL.Networking.ServerClass import Server
from WSUSSL.World.model import Model as wm
#from WSUSSL.World.receiver import proto2_ssl_vision_py_receiver as receiver
from WSUSSL.World.receiver import grsim_coms 
from WSUSSL.World.receiver import ssl_vision_receiver
from WSUSSL.Shared.utils import main as UI
from WSUSSL.TeamControl.Skills.GoTowards import GoTowards as goto


if __name__ ==  '__main__':
    # call world.model wm
    world = wm()
    #receiver = ssl_vision_receiver(world)
    receiver = grsim_coms(world)
    server = Server(0)
    while True:
        receiver.listen_world()
