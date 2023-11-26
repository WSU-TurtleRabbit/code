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


// Main function (for testing)
int main() {
    UdpClient client("127.0.0.1", 4711);  // Replace with your server IP and port
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

