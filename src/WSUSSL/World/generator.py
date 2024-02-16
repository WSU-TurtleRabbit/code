### This file is only used to generate local data for the world model ###
### Testing purposes Only ###

import socket
from WSUSSL.World.proto2 import ssl_vision_wrapper_pb2
from WSUSSL.World.proto2 import ssl_vision_geometry_pb2
from WSUSSL.World.proto2 import ssl_vision_detection_pb2

import random
import time

HOST = '127.0.0.1'
PORT  = 50514

def send_test_message(message):
    vision_ssl_proto2_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    vision_ssl_proto2_socket.sendto(message, (HOST, PORT))

if __name__ == '__main__':
    while True:
        confidence = random.uniform(0.1, 3.0)
        x = random.uniform(0.1, 3.0)
        y = random.uniform(0.1, 3.0)
        z = random.uniform(0.1, 3.0)
        pixel_x = random.uniform(0.1, 3.0)
        pixel_y = random.uniform(0.1, 3.0)

        detection = ssl_vision_detection_pb2.SSL_DetectionBall(
            confidence=confidence, x=x, y=y, z=z, pixel_x=pixel_x, pixel_y=pixel_y
        )

        frame_number = random.randint(0, 10)
        t_capture = random.uniform(0.1, 3.0)
        t_sent = random.uniform(0.1, 3.0)
        camera_id = random.randint(0, 10)
        balls = [detection]
        detectionframe = ssl_vision_detection_pb2.SSL_DetectionFrame(
            frame_number=frame_number, t_capture=t_capture, t_sent=t_sent,
            camera_id=camera_id, balls=balls
        )

        wrapperpacket = ssl_vision_wrapper_pb2.SSL_WrapperPacket(
            detection=detectionframe
        )
        print(wrapperpacket)

        send_test_message(wrapperpacket.SerializeToString())
        time.sleep(5)
