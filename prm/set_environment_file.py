import json

moving_robot = 0 #robot_id
target_position = '1000,-300' #mm
# The buffer should be at least the robot diameter plus some safety distance
buffer = 250 #mm 

# Parse JSON data
with open("prm/SSL_vision_output.json") as f:
    data = json.load(f)

#ä get robot data
all_robots_data = data.get("robots_blue", []) + data.get("robots_yellow", [])

# Check if moving robot is detected
moving_robot_found = any(robot["robot_id"] == moving_robot for robot in all_robots_data)

# Create a txt file
output_file_path = "prm/environment.txt"

# Check if moving robot is found
if moving_robot_found:
    # Write data to the txt file
    with open(output_file_path, "w") as output_file:
        # Print start and end node positions
        output_file.write(f"{round(all_robots_data[0]['x'])},{round(all_robots_data[0]['y'])};{target_position}\n")

        # Write data for each robot
        for robot in all_robots_data:
            if robot["robot_id"] != moving_robot:
                x_position = round(robot["x"])
                y_position = round(robot["y"])

                # Write row to the file (topleft and bottomright corners of obstacles)
                output_file.write(f"{x_position-buffer},{y_position+buffer};{x_position+buffer},{y_position-buffer}\n")
        
        output_file.write("-1") # necessary at the end of environment file

    print(f"Data has been written to {output_file_path}")
else:
    print(f"Moving robot with ID {moving_robot} not found in the JSON data. Aborting program.")
