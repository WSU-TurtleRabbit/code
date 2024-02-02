#! /usr/bin/env python3
from WSUSSL.Networking.ServerClass import Server
from WSUSSL.World.model import Model as wm
from WSUSSL.Shared.utils import main as UI

if __name__ ==  '__main__':
    # call world.model wm
    world = wm()
    # connect to other script (sending wm)
    server = Server(6)
    server.send_action(UI())
