#! /usr/bin/env python3

import asyncio

import TurtleRabbitSSL

if __name__ == '__main__':
    wheels = TurtleRabbitSSL.WheelController()
    asyncio.run(wheels.run())