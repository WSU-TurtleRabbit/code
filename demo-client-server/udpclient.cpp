#include "udpclient.hpp"
#include <thread>
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <fcntl.h>

UdpClient::UdpClient(const std::string& server_ip, int server_port)
{
    std::cerr << "UDP client connecting to " << server_ip << ":" << server_port << std::endl;
    setServerAddress(server_ip, server_port);
}

UdpClient::~UdpClient() {
    close(sockfd);
}

void
UdpClient::sendMessage(const std::string& message) const
{
    sendto(sockfd, message.c_str(), message.size(), 0, 
           (struct sockaddr *)&server_addr, sizeof(server_addr));
}

std::string
UdpClient::receiveMessage() {
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

void
UdpClient::sendInitialMessage() const
{
    std::string message("Hello Turtle");
    sendMessage(message);
}

bool
UdpClient::waitForTurtle(int timeOutMS)
{
    auto startTime = std::chrono::steady_clock::now();
    while (std::chrono::steady_clock::now() - startTime < std::chrono::milliseconds(timeOutMS))
    {
        std::string message = receiveMessage();
        if (message == "Hello Rabbit")
            return true;
    }
    return false;
}

void
UdpClient::setServerAddress(const std::string& server_ip, int server_port)
{
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);
    inet_pton(AF_INET, server_ip.c_str(), &server_addr.sin_addr);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Error opening socket." << std::endl;
        exit(EXIT_FAILURE);
    }
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

void
UdpClient::receiveUpdates()
{
    int reconnectAttempts = 0;
    const int maxReconnectAttempts = 3;

    auto lastMessageTime = std::chrono::steady_clock::now();
    isConnected = true;

    while (isConnected && reconnectAttempts < maxReconnectAttempts)
    {
        std::string message = receiveMessage();

        if (!message.empty())
        {
            std::cout << "Received message: " << message << std::endl;
            lastMessageTime = std::chrono::steady_clock::now();
            reconnectAttempts = 0;
        } else {
            if (std::chrono::steady_clock::now() - lastMessageTime > std::chrono::seconds(10))
            {
                reconnectAttempts++;
                std::cout << "Message timeout. Trying to re-establish communication with server..." << std::endl;
                sendInitialMessage();
                bool c = waitForTurtle(5000);
                if (!c)
                    std::cout << "unsuccessful (" << reconnectAttempts << ")\n";
                lastMessageTime = std::chrono::steady_clock::now();
            }
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    if (reconnectAttempts >= maxReconnectAttempts)
    {
        std::cerr << "Failed to reconnect to the server. Terminating client." << std::endl;
        isConnected = false;
    }
}

// Main function (for testing)
int
main(int argc, char *argv[])
{
    std::string serverIP("127.0.0.1");
    int serverPort = 4711;
    
    if (argc > 1)
    {
        serverIP = argv[1]; 
    }
    UdpClient client(serverIP, serverPort);

    client.sendInitialMessage();

    bool connected = client.waitForTurtle(5000);
    if (connected)
    {
        std::thread receiveThread(&UdpClient::receiveUpdates, &client);
        receiveThread.join();
    }
    else 
    {
        std::cerr << "Failed to connect to server at " << serverIP << ":" << std::to_string(serverPort) << "\n";
    }


    return 0;
}
