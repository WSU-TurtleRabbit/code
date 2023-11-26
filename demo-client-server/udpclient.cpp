#include "udpclient.hpp"
#include <thread>
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <fcntl.h>

UdpClient::UdpClient(const std::string& server_ip, int server_port) {
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Error opening socket." << std::endl;
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);
    inet_pton(AF_INET, server_ip.c_str(), &server_addr.sin_addr);

    // set the socket to non-blocking
    int flags = fcntl(sockfd, F_GETFL, 0);
    if (flags == -1) {
        std::cerr << "Error getting socket flags." << std::endl;
        exit(EXIT_FAILURE);
    }
    if (fcntl(sockfd, F_SETFL, flags | O_NONBLOCK) == -1) {
        std::cerr << "Error setting socket to non-blocking mode." << std::endl;
        exit(EXIT_FAILURE);        
    }
}

UdpClient::~UdpClient() {
    close(sockfd);
}

void UdpClient::sendMessage(const std::string& message) {
    sendto(sockfd, message.c_str(), message.size(), 0, 
           (struct sockaddr *)&server_addr, sizeof(server_addr));
}

std::string UdpClient::receiveMessage() {
    char buffer[1024];
    struct sockaddr_in from_addr;
    socklen_t from_len = sizeof(from_addr);

    ssize_t n = recvfrom(sockfd, buffer, 1024, 0, (struct sockaddr *)&from_addr, &from_len);
    if (n > 0) {
        buffer[n] = '\0';
        return std::string(buffer);
    } else if (errno != EWOULDBLOCK && errno != EAGAIN) {
        std::cerr << "No message received. Error: " << strerror(errno) << std::endl;
    }
    return "";
}

std::string UdpClient::listenForBroadcast(int broadcastPort) {
    int broadcastSocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (broadcastSocket < 0) {
        std::cerr << "Error opening broadcast socket." << std::endl;
        return "";
    }

    struct sockaddr_in listenAddr;
    memset(&listenAddr, 0, sizeof(listenAddr));
    listenAddr.sin_family = AF_INET;
    listenAddr.sin_port = htons(broadcastPort);
    listenAddr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(broadcastSocket, (struct sockaddr *)&listenAddr, sizeof(listenAddr)) < 0) {
        std::cerr << "Error binding broadcast socket." << std::endl;
        close(broadcastSocket);
        return "";
    }

    char buffer[1024];
    struct sockaddr_in senderAddr;
    socklen_t senderAddrLen = sizeof(senderAddr);

    ssize_t n = recvfrom(broadcastSocket, buffer, sizeof(buffer), 0, 
                         (struct sockaddr *)&senderAddr, &senderAddrLen);
    close(broadcastSocket);

    if (n > 0) {
        buffer[n] = '\0';
        return std::string(inet_ntoa(senderAddr.sin_addr)); // Return the sender's IP
    }

    return "";
}

void UdpClient::setServerAddress(const std::string& server_ip, int server_port) {
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);
    inet_pton(AF_INET, server_ip.c_str(), &server_addr.sin_addr);
}


// Main function (for testing)
int main(int argc, char *argv[]) {
    std::string serverIP;
    int serverPort = 4711;
    
    if (argc > 1) {
        serverIP = argv[1]; 
    }

    UdpClient client(serverIP.empty() ? "0.0.0.0" : serverIP, serverPort); 

    if (serverIP.empty()) {
        // if there's no server IP, we listen for broadcasts (server discovery)
        serverIP = client.listenForBroadcast(50021);
        if (serverIP.empty()) {
            std::cerr << "Failed to discover server via broadcast." << std::endl;
            return 1;
        }
        // Update client with discovered server IP
        client.setServerAddress(serverIP, serverPort);    
    }
    
    client.sendMessage("Hello, UDP Server!");

    while (true) {
        std::string message = client.receiveMessage();
        if (!message.empty()) {
            std::cout << "Received message: " << message << std::endl;
            // send ack to server
            client.sendMessage("Ack: " + message);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    return 0;
}
