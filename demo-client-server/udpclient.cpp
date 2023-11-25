#include "udpclient.hpp"
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>

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
}

UdpClient::~UdpClient() {
    close(sockfd);
}

void UdpClient::sendMessage(const std::string& message) {
    sendto(sockfd, message.c_str(), message.size(), 0, 
           (struct sockaddr *)&server_addr, sizeof(server_addr));
}

// Main function (for testing)
int main() {
    UdpClient client("127.0.0.1", 4711);  // Replace with your server IP and port
    client.sendMessage("Hello, UDP Server!");

    return 0;
}

