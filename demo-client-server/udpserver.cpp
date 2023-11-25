#include "udpserver.hpp"
#include <iostream>
#include <cstring>
#include <unistd.h>

UdpServer::UdpServer(int port) : running(false) {
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Error opening socket." << std::endl;
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);
}

UdpServer::~UdpServer() {
    stop();
    close(sockfd);
}

void UdpServer::start() {
    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Binding failed." << std::endl;
        exit(EXIT_FAILURE);
    }

    running = true;
    std::thread listener([this] { this->listen(); });  // Using a lambda function
    listener.detach();
}

void UdpServer::stop() {
    running = false;
}

void UdpServer::listen() {
    char buffer[1024];
    struct sockaddr_in client_addr;
    socklen_t len = sizeof(client_addr);

    while (running) {
        ssize_t n = recvfrom(sockfd, buffer, 1024, 0, (struct sockaddr *)&client_addr, &len);
        if (n > 0) {
            buffer[n] = '\0';
            std::lock_guard<std::mutex> lock(mutex);
            std::cout << "Received message: " << buffer << std::endl;
        }
    }
}

// Main function (for testing)
int main() {
    UdpServer server(4711);
    server.start();

    std::cout << "UDP server is running. Press Enter to stop." << std::endl;
    std::cin.get();

    server.stop();
    return 0;
}


