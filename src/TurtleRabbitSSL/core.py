import moteus
import moteus_pi3hat
import math
import asyncio

import numpy as np

def poll_laptop():
    vx = 1.
    vy = 1.
    theta = np.pi/2
    return vx, vy, theta

class WheelController:
    async def __init__(self):
        self.transport = moteus_pi3hat.Pi3HatRouter(
            motor_bus_map = {
                0: [0],
                1: [1],
                2: [2],
                3: [3]
            }
        )

        self.motors = {
            id : moteus.Controller(id=id, transport=self.transport)
            for id in range(4)
        }

        await self.transport.cycle(x.make_stop() for x in self.motors.values())

    async def run(self, delay=.2):
        while True:
            vx, vy, theta = poll_laptop()
            u = self.calc_u(vx, vy, theta)
            results = await self.transport.cycle([
                self.motor[idx].make_position(position=math.nan,
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

    @staticmethod
    def calc_u(vx, vy, theta, R=10., r=5.):
        Vb = np.array([theta, vx, vy])
        H = np.array([[-R, -R, -R, -R],
                [np.cos(np.pi/4), np.cos(np.pi/4), -np.cos(3*np.pi/4), -np.cos(3*np.pi/4)],
                [np.sin(np.pi/4), -np.sin(np.pi/4), -np.sin(3*np.pi/4), np.sin(3*np.pi/4)],
                ])
        
        # [H (transposed) (dot) Vb]/r
        u = (H.T@Vb)/r
        return u

    