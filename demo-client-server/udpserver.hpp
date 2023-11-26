// -*- mode: c++ -*-
#ifndef UDPSERVER_HPP
#define UDPSERVER_HPP

#include <atomic>
#include <thread>
#include <mutex>
#include <string>
#include <unordered_map>
#include <netinet/in.h>

class UdpServer {
public:
    UdpServer(int comm_port, int broadcast_port, int initial_life_counter = 10);
    ~UdpServer();

    void start();
    void stop();

private:
    const int INITIAL_LIFE_COUNTER;

    struct NetworkAddresses {
        struct sockaddr_in serverAddr;
        struct sockaddr_in broadcastAddr;

        NetworkAddresses() {
            memset(&serverAddr, 0, sizeof(serverAddr));
            memset(&broadcastAddr, 0, sizeof(broadcastAddr));
        }
    };
       
    struct BotInfo {
        int id;
        struct sockaddr_in address;
        int counter;
        std::chrono::steady_clock::time_point last_ack;
        // whatever else we need (eg uniform number, different from internal ID)
    };

    int sockfd;
    int broadcast_fd;
    struct sockaddr_in server_addr;

    bool broadcast_enabled;

    NetworkAddresses server;   

    int comm_port;
    int broadcast_port;

    std::atomic<bool> running;
    std::mutex bots_mutex;

    std::unordered_map<std::string, BotInfo> bots;
    int next_bot_id;

    std::thread update_thread;
    std::thread broadcast_thread;    

    void update();
    void listen();
    void handleBot(const struct sockaddr_in& bot_addr);
    void handleAcknowledgement(const std::string& message, const struct sockaddr_in& bot_addr);
    std::string getBotKey(const struct sockaddr_in& bot_addr);
    void sendMessageToBot(const std::string& message, const struct sockaddr_in& bot_addr);
    NetworkAddresses getNetworkAddresses();
    void broadcastPresence();

};

#endif // UDPSERVER_HPP
