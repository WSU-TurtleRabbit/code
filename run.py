#! /usr/bin/env python3

from WSUSSL.Networking.ServerClass import Server
from WSUSSL.World.model import Model
from WSUSSL.World.receiver import grsim_coms 
from WSUSSL.World.receiver import ssl_vision_receiver
from WSUSSL.TeamControl.skillcontroller import SkillControl

from multiprocessing import Process, Pipe, freeze_support

import argparse


if __name__ ==  '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--rev', '-r', type=int)
    args = parser.parse_args()
    kwargs  = vars(args)
    
    
    world = Model()
    server = Server(0)
    
    # r = int(input("1. ssl-vision 2.grsim"))
    # match r:
    #     case 1:
    #         receiver = ssl_vision_receiver(world)
    #     case 2:
    #         receiver = grsim_coms(world)

    match kwargs['rev']:
        case 1:
            receiver = ssl_vision_receiver(world)
        case 2:
            receiver = grsim_coms(world)
    
    a_pair_of_socks = receiver.pipe()
    world_update = Process(target=receiver.listen_world)

    skills = SkillControl(a_pair_of_socks, [])
    different_pipe_connection = skills.pipe()
    team_controller = Process(target=skills.run_skill_loop)

    server = Server(different_pipe_connection)

    robot_receive = Process(target=server.listen_udp)
    send_action_to_robot = Process(target=server.run)

    team_controller.start()
    world_update.start()
    robot_receive.start()
    send_action_to_robot.start()

    team_controller.join()
    world_update.join()
    robot_receive.join()
    send_action_to_robot.join()

    print('Whoops??! Something went really wrong for this to print?!')


    
