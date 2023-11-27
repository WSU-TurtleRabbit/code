#! /usr/bin/env python3 -B

import asyncio
from asyncio.queues import QueueEmpty, QueueFull
import multiprocessing
import concurrent.futures

from TurtleRabbitSSL.Controllers.proto2 import messages_turtlerabbit_ssl_agent_pb2
# from TurtleRabbitSSL.Controllers.pi3hat import MotionController

global q
global flag_q_not_empty

q = asyncio.Queue(maxsize=2)

# def worker():
#     p = multiprocessing.Process(target=, daemon=True)

def foo(q):
    # turtlerabbit_ssl_agent = messages_turtlerabbit_ssl_agent_pb2.AgentCommandWrapper()
    # return turtlerabbit_ssl_agent.FromString(q)
    return q

def worker():
    global flag_q_not_empty, q
    with concurrent.futures.ProcessPoolExecutor(2) as process_pool:
        work = []
        while not q.empty():
            work.append(q.get_nowait())

        flag_q_not_empty.clear()
        results = list(process_pool.map(foo, work))
    return results

async def work():
    global flag_q_not_empty
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(1) as thread_pool:
        while True:
            await flag_q_not_empty.wait()
            results = await loop.run_in_executor(
                thread_pool, worker)
            
            print(results)

    
class ListenerProtocolT(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        global flag
        loop = asyncio.get_running_loop()
        try:
            loop.call_soon_threadsafe(q.put_nowait, data)
            flag_q_not_empty.set()
        except QueueFull:
            pass

    def error_received(self, exc):
        raise exc


class PrimaryController:
    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port

        self.loop = None

    def start(self):
        global flag_q_not_empty
        loop = asyncio.get_event_loop()
        flag_q_not_empty = asyncio.Event()

        transport = loop.create_datagram_endpoint(lambda: ListenerProtocolT(), 
                                                            local_addr=(self.ip_addr, self.port))
            
        loop.run_until_complete(transport)
        loop.run_until_complete(work())
        loop.run_forever()

if __name__ == '__main__':
    client = PrimaryController('127.0.0.1', 50514)
    client.start()
    # asyncio.run(work())