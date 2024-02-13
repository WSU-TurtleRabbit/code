#! /usr/bin/env python3

from WSUSSL.Networking.ServerClass import Server
from WSUSSL.World.model import Model
from WSUSSL.World.receiver import grsim_coms 
from WSUSSL.World.receiver import ssl_vision_receiver
from WSUSSL.TeamControl.skillcontroller import SkillControl

from multiprocessing import Process, Pipe, freeze_support

import argparse


if __name__ ==  '__main__':

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--rev', '-r', type=int)
    # args = parser.parse_args()
    # kwargs  = vars(args)
    
    
    world = Model()
    
    r = int(input("1. ssl-vision 2.grsim"))
    match r:
        case 1:
            receiver = ssl_vision_receiver(world)
        case 2:
            receiver = grsim_coms(world)

    # match kwargs['rev']:
    #     case 1:
    #         receiver = ssl_vision_receiver(world)
    #     case 2:
    #         receiver = grsim_coms(world)
    world_pipe = receiver.pipe()
    world_update = Process(target=receiver.listen_world)

    skills = SkillControl(world_pipe, [])
    skill_controller = Process(target=skills.run_skill_loop)

   

    world_update.start()
    skill_controller.start()

    world_update.join()
    skill_controller.join()

    print('Whoops??! Something went really wrong for this to print?!')


    
