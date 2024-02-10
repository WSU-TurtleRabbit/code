
import sys
import numpy as np
import argparse
from WSUSSL.PRM import PRMController, Obstacle, Utils


def main(args):

    parser = argparse.ArgumentParser(description='PRM Path Planning Algorithm')
    parser.add_argument('--numSamples', type=int, default=47, metavar='N',
                        help='Number of sampled points')
    args = parser.parse_args()

    numSamples = args.numSamples

    env = open("environment.txt", "r")
    l1 = env.readline().split(";")

    current = list(map(int, l1[0].split(",")))
    destination = list(map(int, l1[1].split(",")))

    print("Current: {} Destination: {}".format(current, destination))

    print("****Obstacles****")
    allObs = []
    for l in env:
        if(";" in l):
            line = l.strip().split(";")
            topLeft = list(map(int, line[0].split(",")))
            bottomRight = list(map(int, line[1].split(",")))
            obs = Obstacle(topLeft, bottomRight)
            obs.printFullCords()
            allObs.append(obs)

    utils = Utils(x_min=-5040/2,y_min=-2760/2,x_max=5040/2,y_max=2760/2) # Change this according to the field dimensions
#    utils.setBoundaries(allObs, current, destination, 
#                        x_margin = 50, y_margin = 10)
    x_min, y_min, x_max, y_max = utils.getBoundaries()
    
    utils.drawMap(allObs, current, destination)

    prm = PRMController(numSamples, allObs, current, destination)
    prm.setBoundaries(x_min, y_min, x_max, y_max)
    # Initial random seed to try
    initialRandomSeed = 0
    prm.runPRM(initialRandomSeed)


if __name__ == '__main__':
    main(sys.argv)
