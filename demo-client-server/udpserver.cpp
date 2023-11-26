#include "udpserver.hpp"
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <chrono>
#include <sstream>

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <ifaddrs.h>
#include <net/if.h>

UdpServer::UdpServer(int comm_port, int initial_life_counter)
: comm_port(comm_port),
  INITIAL_LIFE_COUNTER(initial_life_counter),
  running(false), next_bot_id(0) {

    // set up communication socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Error opening communication socket." << std::endl;
        exit(EXIT_FAILURE);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(comm_port);
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

    update_thread = std::thread(&UdpServer::update, this);
}

void
UdpServer::stop() {
    running = false;
    if (update_thread.joinable()) {
        update_thread.join();
    }
}

void UdpServer::listen() {
    char buffer[1024];
    struct sockaddr_in bot_addr;
    socklen_t len = sizeof(bot_addr);

    while (running) {
        ssize_t n = recvfrom(sockfd, buffer, 1024, 0, (struct sockaddr *)&bot_addr, &len);
        if (n > 0) {
            buffer[n] = '\0';
            std::string message(buffer);

            if (message.rfind("Ack: ", 0) == 0) {
                handleAcknowledgement(message, bot_addr);
            }
            else {
                // Process the received message here
                handleBot(bot_addr);
            }
        }
    }
}

void UdpServer::update() {
    while (running) {
        auto now = std::chrono::system_clock::now();
        auto now_c = std::chrono::system_clock::to_time_t(now);
        int counter = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count() % 1000;

        std::stringstream ss;
        ss << "Time: " << now_c << ", Counter: " << counter;

        std::lock_guard<std::mutex> guard(bots_mutex);
        for (auto it = bots.begin(); it != bots.end(); ) {
            std::cout << "Sending to " << it->second.id << " " << ss.str() << "\n";
            sendMessageToBot(ss.str(), it->second.address);

            // decrement alive counter
            if (--(it->second.counter) <= 0) {
                // Remove bot because we do not seem to get acks anymore
                std::cout << "RIP bot #" << it->second.id << " seems lost, removing from updates\n";
                it = bots.erase(it);
            } else {
                ++it;
            }
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(500)); // update twice per second
    }
}

void UdpServer::sendMessageToBot(const std::string& message, const struct sockaddr_in& bot_addr) {
    auto x = sendto(sockfd, message.c_str(), message.size(), 0, (const struct sockaddr*)&bot_addr, sizeof(bot_addr));
    if (x == -1) {
        std::cout << "Send message " << message << " return code " << strerror(errno) << "\n";

    }
}

void UdpServer::handleBot(const struct sockaddr_in& bot_addr) {
    std::string key = getBotKey(bot_addr);

    std::lock_guard<std::mutex> guard(bots_mutex);
    if (bots.find(key) == bots.end()) {
        // New bot
        bots[key] = BotInfo{next_bot_id++, bot_addr, INITIAL_LIFE_COUNTER};    
        std::cout << "New bot connected: Internal ID " << bots[key].id << std::endl;
        
    }

    // Handle bot-specific actions
}

std::string UdpServer::getBotKey(const struct sockaddr_in& bot_addr) {
    char bot_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &bot_addr.sin_addr, bot_ip, INET_ADDRSTRLEN);
    return std::string(bot_ip) + ":" + std::to_string(ntohs(bot_addr.sin_port));
}

// Reset counter and update last_ack when an ack is received
void UdpServer::handleAcknowledgement(const std::string& message, const struct sockaddr_in& bot_addr) {
    std::string key = getBotKey(bot_addr);
    std::lock_guard<std::mutex> guard(bots_mutex);
    if (bots.find(key) != bots.end()) {
        bots[key].counter = INITIAL_LIFE_COUNTER;  // Reset to the initial value
    }
}

std::string getLocalIPAddress() {
    struct ifaddrs *interfaces = nullptr;
    struct ifaddrs *addr = nullptr;
    std::string ipAddress = "Not found";

    if (getifaddrs(&interfaces) == -1) {
        std::cerr << "Failed to get network interfaces" << std::endl;
        return ipAddress;
    }

    for (addr = interfaces; addr != nullptr; addr = addr->ifa_next) {
        if (addr->ifa_addr && addr->ifa_addr->sa_family == AF_INET) { // Check for IPv4
            // Skip the loopback interface
            if (strcmp(addr->ifa_name, "lo") != 0) {
                ipAddress = inet_ntoa(((struct sockaddr_in *)addr->ifa_addr)->sin_addr);
                break;
            }
        }
    }

    freeifaddrs(interfaces);
    return ipAddress;
}


// Main function (for testing)
int main() {
    UdpServer server(4711);
    server.start();

    std::cin.get();

    server.stop();
    return 0;
}
