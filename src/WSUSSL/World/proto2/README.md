# Common : 
    Contains : Robot basic info : 
    1. Team color
    2. Division 
    3. id

# SSL - Vision 
    Contains : 
    
    1. Detection Data
        1. frame Data 
            - frame_number
            - t_capture 
            - t_sent
            - camera_id

        2. Detection of each ball (in balls): 
            - confidence
            - area
            - x
            - y
            - z
            = pixel_x
            - pixel_y
        3. Detection of each Robot (in each team) [robot_yellow,robot_blue]
            - confidence
            - robot_id
            - x 
            - y
            - orientation (o)
            - pixel_x
            - pixel_y
            - height
    
    2. Geometry Data
        1. field
            1. field Lines :1. p1, p2 : x, y, 2. Thickness
                - Top Touch Line
                - Bottom Touch Line
                - Left Goal Line
                - Right Goal Line
                - Half way Line
                - Centre Line
                - Left Penalty Stretch
                - Right Penalty Stretch 
                - Left Field Left Penalty Stretch 
                - Left Field Right Penalty Stretch 
                - Right Field Right Penalty Stretch
                - Right Field Left Penalty Stretch 
                - Centre Circle
        2. Calibration : Calib
            - camera_id
            - focal_length
            - principal_point_x
            - principal_point_y
            - distortion
            - q0
            - q1 
            - q2
            - q3
            - q4
            - tx
            - ty
            - tz
            - derived_camera_world_tx
            - derived_camera_world_ty
            - derived_camera_world_tz

# gr Sim 
    1. commands : sending to gr Sim
    2. packet : recieves from gr Sim