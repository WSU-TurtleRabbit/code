#! /usr/bin/env python3 -B

import asyncio
from asyncio.queues import QueueEmpty, QueueFull
import multiprocessing
import functools

from TurtleRabbitSSL.Controllers.proto2 import messages_turtlerabbit_ssl_agent_pb2
# from TurtleRabbitSSL.Controllers.pi3hat import MotionController


global loop
global q
global flag

q = asyncio.Queue(maxsize=2)

class ListenerProtocolT(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        global loop, flag
        try:
            loop.call_soon_threadsafe(q.put_nowait, data)
            flag.set()
        except QueueFull:
            pass

    def error_received(self, exc):
        raise exc 


class PrimaryController:
    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port

        self.pool = multiprocessing.Pool()

    def start(self):
        global loop, flag
        loop = asyncio.get_event_loop()
        flag = asyncio.Event()


        endpoint = loop.create_datagram_endpoint(ListenerProtocolT, local_addr=(self.ip_addr, self.port))
        loop.run_until_complete(endpoint)
        loop.create_task(self.decode())
        loop.run_forever()

    async def decode(self):
        global q, loop
        while True:
            await flag.wait()
            item = q.get_nowait()
            turtlerabbit_ssl_agent = messages_turtlerabbit_ssl_agent_pb2.AgentCommandWrapper()
            command = turtlerabbit_ssl_agent.FromString(item)
            print(command)
            flag.clear()


if __name__ == '__main__':
    client = PrimaryController('127.0.0.1', 50514)
    client.start()