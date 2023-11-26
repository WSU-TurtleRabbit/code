#! /usr/bin/env python3
import socket
import asyncio

from TurtleRabbitSSL.proto2 import messages_robocup_ssl_wrapper_pb2, messages_robocup_ssl_detection_pb2, messages_robocup_ssl_wrapper_tracked_pb2, messages_robocup_ssl_detection_tracked_pb2
import google.protobuf

HOST = '127.0.0.1'
PORT  = 514

import random

def send_test_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.sendto(message, (HOST, PORT))


async def main():
    while True:
        time = random.uniform(0.1, 3.0)
        await asyncio.sleep(time)
        confidence=0.1 + time
        x=1.2+time
        y=.2+time
        pixel_x=124.
        pixel_y=156.

        message_detectionball = messages_robocup_ssl_detection_pb2.SSL_DetectionBall(confidence=confidence, 
                                                                                     x=x, 
                                                                                     y=y, 
                                                                                     pixel_x=pixel_x, 
                                                                                     pixel_y=pixel_y)
        frame_number=1
        t_capture=1.2 + time
        t_sent=.3 + time
        camera_id=1
        balls=[message_detectionball]


        message_detectionframe = messages_robocup_ssl_detection_pb2.SSL_DetectionFrame(
            frame_number=frame_number, 
            t_capture=t_capture, 
            t_sent=t_sent, 
            camera_id=camera_id, 
            balls=balls)
        
        message_wrapper = messages_robocup_ssl_wrapper_pb2.SSL_WrapperPacket(
            detection=message_detectionframe)
        
        send_test_message(message_wrapper.SerializeToString())
        
if __name__ == '__main__':
    asyncio.run(main())
