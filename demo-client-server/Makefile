all: client server

client: udpclient.cpp udpclient.hpp
	g++ -std=c++11 -o client udpclient.cpp

server: udpserver.cpp udpserver.hpp
	g++ -std=c++11 -o server udpserver.cpp

clean:
	rm -f client server *~
