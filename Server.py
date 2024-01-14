# import
from ServerClass import Server  
import time


## MAIN ###
    # This is the main function of the serverClass
    # When this class first started, it will run the following

def main() : 
    # initiate socket
    server = Server()
    server.broadcast()
    server.ping_all()
    #server.pingAll()
    



if __name__ == "__main__" : 
    main()