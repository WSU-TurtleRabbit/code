'''
coffee backwards is eeffoc-
'''
import moteus
import moteus_pi3hat
import math
import asyncio
import json
import os

import numpy as np
from TurtleRabbitSSL.utils import redirect_print_to_log

def poll_laptop():
    vx = 1.
    vy = 1.
    theta = np.pi/2
    return (vx, vy, theta)

class WheelController:
    async def __init__(self):
        self.load_from_config(os.path.join(os.getcwd(), 'example.config.json'))
 

        self.transport = moteus_pi3hat.Pi3HatRouter(
            servo_bus_map = {
                0: [0],
                1: [1],
                2: [2],
                3: [3],
            }
        )

        self.servos = {
            id : moteus.Controller(id=id, transport=self.transport)
            for id in range(4)
        }

        await self.transport.cycle(x.make_stop() for x in self.servos.values())

    @redirect_print_to_log('log.txt')
    async def run(self, delay=.2):
        while True:
            vx, vy, theta = poll_laptop()
            u = self.calc_u(vx, vy, theta)
            results = await self.transport.cycle([
                self.servos[idx].make_position(position=math.nan,
                                              velocity=u[idx],
                                              query=True)
                for idx in range(4)
            ])

            print(", ".join(
                f"({result.arbitration_id} " +
                f"{result.values[moteus.Register.POSITION]} " +
                f"{result.values[moteus.Register.VELOCITY]})"
                for result in results))
            
            await asyncio.sleep(delay)

    def calc_u(self, vx, vy, theta):
        '''
        "Modern Robotics: Mechanics, Planning & Control"
        13.2.1
        
        just leaving this here for no particular reason:
        libgen (dot) rs
        '''
        Vb = np.array([theta, vx, vy])
        H = np.array([[-self.d[0], -self.d[1], -self.d[2], -self.d[3]],
                [np.cos(self.b[0]), np.cos(self.b[1]), -np.cos(self.b[2]), -np.cos(self.b[3])],
                [np.sin(self.b[0]), -np.sin(self.b[1]), -np.sin(self.b[2]), np.sin(self.b[3])],
                ])
        
        # [H (transposed) (dot) Vb]/r
        u = (H.T@Vb)/self.r
        return u
    
    def load_from_config(self, fname):
        if not os.path.exists(fname):
            raise FileExistsError(f".json config doesn't exist ({fname=})")
        
        with open(fname) as f:
            config = json.load(f)
        f.close()

        if not 'servo' in config:
            raise KeyError(f"invaild .json config: key 'servo' not found")
        if not 'dimensions' in config['servo']:
            raise KeyError(f"invaild .json config: 'servo' (sub)key 'dimensions' not found")
        
        dimensions = config['servo']["dimensions"]

        if not 'distance_from_origin' in dimensions:
            raise KeyError(f"invaild .json config: key 'distance_from_origin' not found")

        self.d = dimensions["distance_from_origin"]["values"]

        if not len(self.d) == 4:
            raise ValueError(f"invaild .json config: key 'distance_from_origin' doesn't have enough parameters, need 4, got {len(self.d)}")
        
        self.r = dimensions["wheel_radius"]["values"]

        self.b = dimensions["wheel_slip_angle"]["values"]

        if not len(self.b) == 4:
            raise ValueError(f"invaild .json config: key 'wheel_slip_angle' doesn't have enough parameters, need 4, got {len(self.b)}")
