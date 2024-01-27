#! /usr/bin/env python3
from WSUSSL.Networking.ServerClass import Server
from WSUSSL.Shared.utils import main as interface

if __name__ ==  '__main__':
    # call world.model wm
    # connect to other script (sending wm)

    server = Server()
    server.send_message(interface())
