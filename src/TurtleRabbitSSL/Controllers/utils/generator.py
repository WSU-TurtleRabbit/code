#! /usr/bin/env python3
import socket
import asyncio

from TurtleRabbitSSL.Controllers.proto2 import messages_turtlerabbit_ssl_agent_pb2 

HOST = ''
PORT  = 50514

import random

def send_test_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.sendto(message, (HOST, PORT))


async def main():
    while True:
        time = random.uniform(0.1, 3.0)
        await asyncio.sleep(time)
        id = random.randint(0, 32)
        vx = random.uniform(0.1, 3.0)
        vy = random.uniform(0.1, 3.0)
        tfd = random.uniform(0.1, 3.0)
        
        message_wrapper = messages_turtlerabbit_ssl_agent_pb2.RobotAgentCommand(
            id=id, vx=vx, vy=vy, tfd=tfd)
        
        print(message_wrapper)
        print(message_wrapper.SerializeToString())
        send_test_message(message_wrapper.SerializeToString())
        
if __name__ == '__main__':
    asyncio.run(main())
