"""
This example is not working due to an infinity loop at sslvisionreceiver
"""
from sslvisionreceiver import w


current_ball_pos1 = w.get_ball_position()
current_ball_pos2 = w.get_ball_position()
print(current_ball_pos1,current_ball_pos2)

# where will the ball be at 
new_ball_pos = current_ball_pos2 - current_ball_pos1 /0.02