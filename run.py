#! /usr/bin/env python3

import asyncio

import TurtleRabbitSSL

if __name__ == '__main__':
    wheels = TurtleRabbitSSL.Controllers.MotionController()
    asyncio.run(wheels.run())