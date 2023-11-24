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

def poll_laptop():
    vx = 1.
    vy = 1.
    theta = np.pi/2
    return (vx, vy, theta)

class Controller:
    def __init__(self):
        return NotImplementedError
    
    def run(self):
        return NotImplementedError

class WheelController:
    async def __init__(self):
        self.load_from_config(os.path.join(os.getcwd(), 'wheelconfig.json'))
 

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
        Vb = np.array([theta, vx, vy])
        H = np.array([[-self.d[0], -self.d[1], -self.d[2], -self.d[3]],
                [np.cos(self.b[0]), np.cos(self.b[1]), -np.cos(self.b[2]), -np.cos(self.b[3])],
                [np.sin(self.b[0]), -np.sin(self.b[1]), -np.sin(self.b[2]), np.sin(self.b[3])],
                ])
        
        # [H (transposed) (dot) Vb]/r
        u = (H.T@Vb)/self.r
        return u
    
    def load_from_config(self, root):
        with open(root) as f:
            config = json.load(f)
        f.close()
        
        params = config['servo']["dimensions"]

        self.d = params["d"]
        self.r = params["r"]
        self.b = params["b"]