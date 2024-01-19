import socket
import keyboard 
import time

def send_velocity_command(ip, port, W, Vx, Vy):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"{W},{Vx},{Vy}"
    client_socket.sendto(message.encode(), (ip, port))
    client_socket.close()


def control_robot():
    velocity_increment = 0.5  
    W, Vx, Vy = 0, 0, 0
    key_pressed = False

    while True:
        key_pressed = False

        if keyboard.is_pressed('w'):  # Forward
            Vy = velocity_increment
            key_pressed = True
        elif keyboard.is_pressed('s'):  # Backward
            Vy = -velocity_increment
            key_pressed = True
        elif keyboard.is_pressed('a'):  # Left
            Vx = -velocity_increment
            key_pressed = True
        elif keyboard.is_pressed('d'):  # Right
            Vx = velocity_increment
            key_pressed = True
        elif keyboard.is_pressed('q'):  # Spin left
            W = -velocity_increment
            key_pressed = True
        elif keyboard.is_pressed('e'):  # Spin right
            W = velocity_increment
            key_pressed = True
        elif keyboard.is_pressed('esc'):  # Exit
            break

        if key_pressed:
            send_velocity_command(raspberry_pi_ip, port, W, Vx, Vy)
            time.sleep(0.1)

        # Reset velocities to stop if no keys are pressed
        W, Vx, Vy = 0, 0, 0

raspberry_pi_ip = "172.20.10.14"
port = 5005

print("Use WASD to move, Q/E to spin, and ESC to exit.")
control_robot()
