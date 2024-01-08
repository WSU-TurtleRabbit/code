## Developed for the RAM robotics club at Western Sydney University
## by Eren Yilmaz
##
## Motor Control Script
##
## This script will command a 4-omniwheeled 
## robot according to commands it receives over
## a network via UDP. In this script, once the 
## pi3hat bus numbers are set and assigned servo 
## IDs, these are passed along to a chain of functions 
## that require them to send "lists of commands" to the
## servos. You will need the client script to send commands
## to the UDP server in this script. 

import asyncio
import math
import moteus
import moteus_pi3hat
import numpy as np
import time
import socket



# Class for translating the array input into motor
# commands.
class MotorControl:

    def __init__(self, transport, servos):
        self.transport = transport
        self.servos = servos


    # This function converts the robot's velocities to 
    # individual to four angular velocities of the wheels.
    # matrix_A could be [1  0] for omniwheels, but
    # original formula is left for clarity (gamma = slider angle).
    def omniwheel(self, W, Vx, Vy):
        gamma = 0
        beta = np.radians(120)
        beta2 = np.radians(45)
        beta3 = np.radians(-45)
        beta4 = np.radians(-120)

        matrix_A = np.array([1, np.tan(np.radians(gamma))]) /0.05

        #  One matrix multiplication per wheel
        matrix_B = np.array([[np.cos(beta), np.sin(beta)], [-np.sin(beta), np.cos(beta)]])
        matrix_B2 = np.array([[np.cos(beta2), np.sin(beta2)], [-np.sin(beta2), np.cos(beta2)]])
        matrix_B3 = np.array([[np.cos(beta3), np.sin(beta3)], [-np.sin(beta3), np.cos(beta3)]])
        matrix_B4 = np.array([[np.cos(beta4), np.sin(beta4)], [-np.sin(beta4), np.cos(beta4)]])

        matrix_C = np.array([[-0.1, 1, 0], [0.1, 0, 1]])
        matrix_C2 = np.array([[0.1, 1, 0], [0.1, 0, 1]])
        matrix_C3 = np.array([[0.1, 1, 0], [-0.1, 0, 1]])
        matrix_C4 = np.array([[-0.1, 1, 0], [-0.1, 0, 1]])

        velocity_vector = np.array([(W), Vx, Vy])

        # Divide by 2pi to convert radians/sec to hertz (moteus velocity)
        servo1 = (matrix_A @ matrix_B @ matrix_C @ velocity_vector) / (2*math.pi)
        servo2 = (matrix_A @ matrix_B2 @ matrix_C2 @ velocity_vector) / (2*math.pi)
        servo3 = (matrix_A @ matrix_B3 @ matrix_C3 @ velocity_vector) / (2*math.pi)
        servo4 = (matrix_A @ matrix_B4 @ matrix_C4 @ velocity_vector) / (2*math.pi) 
        print()
        print(f"Velocities directly from omniwheel function: servo1: {servo1}, servo2: {servo2}, servo3: {servo3}, servo4: {servo4}")
        print()
        return servo1, servo2, servo3, servo4

    # Brake function: 
    # Sends position=math.nan without a velocity argument to "hold" the motors,
    # followed by a stop command that is sent to all motors. The "timeout" parameter
    # is the length of time the motors are held. Hence, it stops the motor from drifting away.
    async def brake(self, brake_timeout):
        start_time = time.time()
        while time.time() - start_time < brake_timeout:
            await self.transport.cycle([x.make_position(position=math.nan) for x in self.servos.values()])
            await asyncio.sleep(0.02)
        await self.transport.cycle([x.make_stop() for x in self.servos.values()])

    async def execute_command(self, W, Vx, Vy, timeout):

        vel1, vel2, vel3, vel4 = self.omniwheel(W, Vx, Vy)

        commands = [
            self.servos[1].make_position(
                position=math.nan,
                velocity=vel1,
                query=True),
            self.servos[2].make_position(
                position=math.nan,
                velocity=vel2,
                query=True),
            self.servos[3].make_position(
                position=math.nan,
                velocity=vel3,
                query=True),
            self.servos[4].make_position(
                position=math.nan,
                velocity=vel4,
                query=True)
                    ]


        # Move all motors for an increment of time
        # defined by the "timeout" variable.
        start_time = time.time()
        while time.time() -start_time < timeout:
            print("sending commands nao sir")
            print()
            print(f"vel1 from omniwheel function: {vel1}, vel2: {vel2}, vel3: {vel3}, vel4: {vel4}")
            print()
            print(f"List of commands being sent: {commands}")
            results = await self.transport.cycle(commands)
            await asyncio.sleep(0.02)
            print(results)

class UDPServer:
    def __init__(self, ip, port, motor_control):
        self.ip = ip
        self.port = port
        self.motor_control = motor_control
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.ip, self.port))
        self.udp_socket.setblocking(False)


    # UDP server function: it listens on a local network
    # for UDP packets which contain a velocity vector with
    # a value for the "timeout" variable. It parses the message
    # and sends it to the execute_command function for further
    # processing. 
    async def run_server(self):
        print(f"Listening for UDP packets on {self.ip}:{self.port}")
        while True:
            try:
                # Set a short timeout for receiving data
                self.udp_socket.settimeout(0.01) # 10 ms
                data, address = self.udp_socket.recvfrom(1024)
                message = data.decode()
                

                # Clear backlog by attempting to receive until a timeout
                while True:
                    try:
                        self.udp_socket.recvfrom(1024)
                    except socket.timeout:
                        # No more data in buffer: Break loop
                        break

                # Process latest message
                W, Vx, Vy = map(float, message.split(','))
                print(f"Processing W: {W}, Vx: {Vx}, Vy: {Vy}")
                await self.motor_control.execute_command(W, Vx, Vy, 0.2)
                await self.motor_control.transport.cycle([x.make_stop() for x in self.motor_control.servos.values()])
                #await self.motor_control.brake(1)

            except socket.timeout:
                # No data received, continue the loop
                continue
            except BlockingIOError:
                await asyncio.sleep(0.02)
            except Exception as error:
                print(f"Error: {error}")


# Main asynchronous function, sets bus IDs to motors,
# initialises controllers
async def main():

    # Assigns a bus number (jc1, jc2 etc on the pi3hat board)
    # via the Pi3HatRouter method. 
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map = {
            1: [1],
            2: [2],
            3: [3],
            4: [4],

        }
    )



    # Dictionary comprehension for setting 4 Controller instances.
    # The pi3hat transport is passed via the transport object.
    servos = {
        servo_id : moteus.Controller(id=servo_id, transport=transport)
        for servo_id in [1, 2, 3, 4]
    }

    print(servos)
    await transport.cycle([x.make_stop() for x in servos.values()])

    motor_control = MotorControl(transport, servos)

    # Pass the motor_control object to the UDPServer, which sends along to all
    # functions: "servos" (the dictionary comprehension of controller instances), and the 
    # "transport" object, which holds the servo bus map. 
    udp_server = UDPServer("172.20.10.14", 5005, motor_control)
    try:
        # Main loop will start by calling run_server() method
        await udp_server.run_server()
        # More stop commands (just in case)
        await transport.cycle([x.make_stop() for x in servos.values()])
    except Exception as error:
        print(f"Error: {error}")
        await transport.cycle([x.make_stop() for x in servos.values()])


if __name__ == '__main__':
    asyncio.run(main())
