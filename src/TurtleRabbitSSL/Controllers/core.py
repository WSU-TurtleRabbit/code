#! /usr/bin/env python3 -B

import asyncio
from asyncio.queues import QueueEmpty, QueueFull

import functools

from TurtleRabbitSSL.Controllers.proto2 import messages_turtlerabbit_ssl_agent_pb2
from TurtleRabbitSSL.Controllers.pi3hat import MotionController

global loop
global q

q = asyncio.Queue(maxsize=2)

class ListenerProtocolT(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        global loop
        try:
            loop.call_soon_threadsafe(q.put_nowait, data)
        except QueueFull:
            pass

    def error_received(self, exc):
        raise exc 


class PrimaryController:
    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port

    def start(self):
        global loop
        loop = asyncio.get_event_loop()

        endpoint = loop.create_datagram_endpoint(ListenerProtocolT, local_addr=(self.ip_addr, self.port))
        loop.run_until_complete(endpoint)
        loop.create_task(self.decode())
        loop.run_forever()

    async def decode(self):
        global q, loop
        while True:
            if not q.empty():
                item = q.get_nowait()
                turtlerabbit_ssl_agent = messages_turtlerabbit_ssl_agent_pb2.RobotAgentCommand()
                command = turtlerabbit_ssl_agent.FromString(item)
                print(command)
            await asyncio.sleep(.1)

if __name__ == '__main__':
    client = PrimaryController('127.0.0.1', 50514)
    client.start()