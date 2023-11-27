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

UdpServer::UdpServer(int comm_port, int initial_life_counter, int freq)
: comm_port(comm_port),
  INITIAL_LIFE_COUNTER(initial_life_counter), messageFrequency(freq),
  running(false), next_bot_id(0)
{
    // set up communication socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Error opening communication socket." << std::endl;
        exit(EXIT_FAILURE);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(comm_port);

    local_ip = getLocalIPAddress();
    lastResetTime = std::chrono::steady_clock::now() - std::chrono::seconds(10);
}

UdpServer::~UdpServer()
{
    stop();
    close(sockfd);
}

void
UdpServer::start()
{
    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0)
    {
        std::cerr << "Binding failed." << std::endl;
        exit(EXIT_FAILURE);
    }

    running = true;
    std::thread listener([this] { this->listen(); });  // Using a lambda function
    listener.detach();

    update_thread = std::thread(&UdpServer::update, this);
}

void
UdpServer::stop()
{
    running = false;
    if (update_thread.joinable())
    {
        update_thread.join();
    }
}

void
UdpServer::listen()
{
    char buffer[1024];
    struct sockaddr_in bot_addr;
    socklen_t len = sizeof(bot_addr);

    while (running)
    {
        ssize_t n = recvfrom(sockfd, buffer, 1024, 0, (struct sockaddr *)&bot_addr, &len);
        if (n > 0)
        {
            buffer[n] = '\0';
            std::string message(buffer);
            if (message.rfind("Ack: ", 0) == 0)
            {
                handleAcknowledgement(message, bot_addr);
            } else {
                // Process the received message here
                handleBot(bot_addr, message);
            }
        }
    }
}

void
UdpServer::update()
{
    auto nextSendTime = std::chrono::steady_clock::now();

    while (running)
    {
        auto now = std::chrono::steady_clock::now();

        if (now >= nextSendTime)
        {
            if (now - lastResetTime >= std::chrono::seconds(1))
            {
                messageStep = 0;
                lastResetTime = now;
            }
        
            std::string message = "Time: " + std::to_string(std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count()) +
                ", Counter: " + std::to_string(messageStep++);

            // keeping the sleep out of the protected region
            {
                std::lock_guard<std::mutex> guard(bots_mutex);
                for (auto it = bots.begin(); it != bots.end(); )
                {
                    std::cout << "Sending to " << it->second.id << " " << message << "\n";
                    sendMessageToBot(message, it->second.address);

                    // decrement alive counter
                    if (--(it->second.counter) <= 0)
                    {
                        // Remove bot because we do not seem to get acks anymore
                        std::cout << "RIP bot #" << it->second.id << " seems lost, removing from updates\n";
                        it = bots.erase(it);
                    } else {
                        ++it;
                    }
                }
            }

            nextSendTime += std::chrono::milliseconds(1000 / messageFrequency);
        }
        auto timeToSleep = nextSendTime - std::chrono::steady_clock::now();
        if (timeToSleep > std::chrono::milliseconds(0))
        {
            std::this_thread::sleep_for(timeToSleep);
        }
    }
}

void
UdpServer::sendMessageToBot(const std::string& message, const struct sockaddr_in& bot_addr)
{
    auto x = sendto(sockfd, message.c_str(), message.size(), 0, (const struct sockaddr*)&bot_addr, sizeof(bot_addr));
    if (x == -1)
    {
        std::cout << "Send message " << message << " return code " << strerror(errno) << "\n";
    }
}

void
UdpServer::handleBot(const struct sockaddr_in& bot_addr, const std::string& message)
{
    std::string key = getBotKey(bot_addr);

    std::lock_guard<std::mutex> guard(bots_mutex);    
    
    if (bots.find(key) == bots.end()) {
        // New bot
        bots[key] = BotInfo{next_bot_id++, bot_addr, INITIAL_LIFE_COUNTER};    
        std::cout << "New bot connected: Internal ID " << bots[key].id << std::endl;
    }
    if (message == "Hello Turtle")
    {
        std::string ack = "Hello Rabbit";
        sendMessageToBot(ack, bot_addr);
    }

    // Handle bot-specific actions
}

std::string
UdpServer::getBotKey(const struct sockaddr_in& bot_addr)
{
    char bot_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &bot_addr.sin_addr, bot_ip, INET_ADDRSTRLEN);
    return std::string(bot_ip) + ":" + std::to_string(ntohs(bot_addr.sin_port));
}

// Reset counter and update last_ack when an ack is received
void
UdpServer::handleAcknowledgement(const std::string& message, const struct sockaddr_in& bot_addr)
{
    std::string key = getBotKey(bot_addr);

    // Extract the timestamp from the message
    // Assume the message format is "Time: [timestamp], Counter: [counter]"
    auto timePos = message.find("Time: ");
    auto commaPos = message.find(", ", timePos);
    auto counterPos = message.find("Counter: ", commaPos);
    std::string timestampStr = message.substr(timePos + 6, commaPos - (timePos + 6));
    std::string counterStr = message.substr(counterPos + 9);

    long long timestamp = std::stoll(timestampStr);

    std::chrono::steady_clock::time_point sentTime = std::chrono::steady_clock::time_point(std::chrono::milliseconds(timestamp));
    auto now = std::chrono::steady_clock::now();

    // Calculate the round-trip time
    auto roundTripTime = std::chrono::duration_cast<std::chrono::milliseconds>(now - sentTime);
    
    std::lock_guard<std::mutex> guard(bots_mutex);
    // Store the round trip time in the client's statistics
    commStats[key].rtt.push_back(roundTripTime);

    if (bots.find(key) != bots.end())
    {
        bots[key].counter = INITIAL_LIFE_COUNTER;  // Reset to the initial value
    }
}

std::string
UdpServer::getLocalIPAddress() {
    struct ifaddrs *interfaces = nullptr;
    struct ifaddrs *addr = nullptr;
    std::string ipAddress = "Not found";

    if (getifaddrs(&interfaces) == -1)
    {
        std::cerr << "Failed to get network interfaces" << std::endl;
        return ipAddress;
    }

    for (addr = interfaces; addr != nullptr; addr = addr->ifa_next)
    {
        if (addr->ifa_addr && addr->ifa_addr->sa_family == AF_INET)
        { // Check for IPv4
            // Skip loopback interfaces to get a proper IP address
            if (( addr->ifa_flags & IFF_LOOPBACK) == 0)
            {
                ipAddress = inet_ntoa(((struct sockaddr_in *)addr->ifa_addr)->sin_addr);
                break;
            }
        }
    }

    freeifaddrs(interfaces);
    return ipAddress;
}

std::string
UdpServer::serverAddress() const
{
   return local_ip + ":" + std::to_string(comm_port);
}

void
UdpServer::printCommStats() const
{
    for (const auto& pair : commStats)
    {
        double averageRTT = pair.second.getAverageRTT();
        std::cout << "Client " << pair.first << " - Average RTT: " << averageRTT << " ms" << std::endl;
    }
}

// Main function (for testing)
int
main()
{
    UdpServer server(4711, 100, 5);

    std::cout << "[TurtleRabbit server running at " << server.serverAddress() << ". Press <return> to stop." << std::endl;
    
    server.start();
    std::cin.get();
    server.stop();
    server.printCommStats();
    return 0;
}

