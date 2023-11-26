import asyncio
import multiprocessing
import socket
import queue

from TurtleRabbitSSL.proto2 import messages_robocup_ssl_detection_pb2
from TurtleRabbitSSL.proto2 import messages_robocup_ssl_detection_tracked_pb2
from TurtleRabbitSSL.proto2 import messages_robocup_ssl_wrapper_tracked_pb2

global loop
global q
global lock

q = queue.Queue()

class ListenerProtocolT(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        global loop
        loop.ensure_future(self.write_to_q(data))

    def error_received(self, exc):
        raise exc

    def write_to_q(self, item):
        global lock
        yield from lock
        try:
            q.push(item)
        finally:
            lock.release()

class VisionSSLClient:
    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port

    def start(self):
        global lock, loop
        loop = asyncio.get_event_loop()
        lock = asyncio.Lock(loop=loop)

        endpoint = loop.create_datagram_endpoint(ListenerProtocolT, local_addr=(self.ip_addr, self.port))
        loop.run_until_complete(endpoint)
        loop.run_until_complete(self.decode)
        loop.run_forever()

    def decode(self):
        global q, lock
        yield from lock
        try:
            item = q.pop()
        finally:
            lock.release()

        ssl_wrapper = messages_robocup_ssl_wrapper_tracked_pb2.SSL_WrapperPacket()
        ssl_wrapper.ParseFromString(item)

        print(ssl_wrapper)

def main():
    client = VisionSSLClient('127.0.0.1', 514)
    client.start()
