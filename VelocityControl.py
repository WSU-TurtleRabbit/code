# Simple Velocity Control for Moteus
# Author: [Eren Yilmaz]
# Date: [17-09-2023]
# Version: 1.0
# Description: 
# This script prompts the user for maximum values to rotate the motor in opposite directions. 
# It provides feedback by printing the state of the controller to the console.
# Dependencies: moteus, asyncio
# Developed for the RAM Robotics Club at Western Sydney University

import moteus
import math
import asyncio

def get_parameter(prompt):
    #Define function to request velocity values
    value = input(prompt)
    return float(value)

async def main():
    c = moteus.Controller(id=1)
    await c.set_stop()
    velmax = get_parameter("Enter maximum velocity for clockwise motion: ")
    velmin = get_parameter("Enter maximum velocity for anti-clockwise motion: ")

    
    #Main loop
    while True:
        await c.set_stop()
        vel1 = 0.0001
        vel2 = 0.0001
        #Setting initial velocity values

    
        while vel1 <= velmax:
            #Loop for positive rotation
            await asyncio.sleep(0.05)
            vel1 +=0.01
            #Increment vel1 by 0.01 on each iteration
            state = await c.set_position(position=math.nan, velocity=vel1, query=True)
            print(state)
    
        while vel2 <= velmin:
            #Loop for negative rotation
            await asyncio.sleep(0.05)
            vel2 += 0.01
            #Increment vel2 by 0.01 on each iteration
            state = await c.set_position(position=math.nan, velocity=-vel2, query=True)
            print(state)
            
        
if __name__ == '__main__':
    asyncio.run(main())
