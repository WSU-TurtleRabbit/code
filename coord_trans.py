import numpy as np
from numpy import pi
from numpy.linalg import inv

def transformation_matrix(p):
    '''
        input:
            p: robot pose (x, y, theta)
        output:
            transformation matrix (rotation and translation)
    '''

    p[2] = p[2] - pi/2

    c = np.cos(p[2])
    s = np.sin(p[2])

    transformation_matrix = np.array([
        [c, -s, p[0]],
        [s,  c, p[1]],
        [0,  0,    1]
    ])

    return transformation_matrix

def world2robot(w, p):
    '''
        input:
            w: position in the world coordinate system (x,y)
            p: robot pose (x, y, theta)
        output:
            r: position in the robot coordinate system (x,y)
    '''
    trans_matrix = inv(transformation_matrix(p))
    w = np.append(w, 1) # (x,y,1)

    r = np.dot(trans_matrix, w)[:2]

    return r

def robot2world(r, p):
    '''
        input:
            r: position in the robot coordinate system (x,y)
            p: robot pose (x, y, theta)
        output:
            w: position in the robot coordinate system (x,y)
    '''
    trans_matrix = transformation_matrix(p)
    r = np.append(r, 1) # (x,y,1)

    w = np.dot(trans_matrix, r)[:2]

    return w

def main():
    print('----- examples assuming the angle between the y axes ------')
    print('\nball and robot coincide:')
    print("expected output: [0,0]")
    print(world2robot(np.array([10,10]), np.array([10,10,pi])))
    print(world2robot(np.array([10,10]), np.array([10,10,pi/3])))

    print('\nball 1 to robot coord. system:')
    print("expected output: [0,14.14]")
    print(world2robot(np.array([20,20]), np.array([10,10,-pi/4])))
    print(world2robot(np.array([20,10]), np.array([10,0,-pi/4])))

    print('\nball 2 to robot coord. system:')
    print("expected output: [14.14,0]")
    print(world2robot(np.array([20,0]), np.array([10,10,-pi/4])))

    print('\nball 1 to robot coord. system (robot turned):')
    print("expected output: [0,-14.14]")
    print(world2robot(np.array([20,20]), np.array([10,10,-5/4*pi])))
    print(world2robot(np.array([20,20]), np.array([10,10,3/4*pi])))
    print('\nball 2 to robot coord. system (robot turned):')
    print("expected output: [-14.14,0]")
    print(world2robot(np.array([20,0]), np.array([10,10,-5/4*pi])))
    print(world2robot(np.array([20,0]), np.array([10,10,3/4*pi])))

    print('\nball 1 to world coord. system:')
    print("expected output: [20,20]")
    print(robot2world(np.array([0,14.14213562]), np.array([10,10,-pi/4])))
    print('\nball 2 to world coord. system:')
    print("expected output: [20,0]")
    print(robot2world(np.array([14.14213562, 0]), np.array([10,10,-pi/4])))

    print('\nball 3 to robot coord. system:')
    print("expected output: [-10,0]")
    print(world2robot(np.array([20, 10]), np.array([20,0,0])))

if __name__ == "__main__":
    main()
