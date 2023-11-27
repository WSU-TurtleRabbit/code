// -*- mode: c++ -*-
#ifndef UDPSERVER_HPP
#define UDPSERVER_HPP

#include <atomic>
#include <thread>
#include <mutex>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>
#include <netinet/in.h>
#include <cstring>

class UdpServer {
public:
    UdpServer(int comm_port, int initial_life_counter = 10, int freq = 10);
    ~UdpServer();

    void start();
    void stop();

    std::string serverAddress() const;

    void printCommStats() const;
    
private:
    const int INITIAL_LIFE_COUNTER;

    int messageFrequency;

    struct BotInfo {
        int id;
        struct sockaddr_in address;
        int counter;
        std::chrono::steady_clock::time_point last_ack;
        // whatever else we need (eg uniform number, different from internal ID)
    };

    struct CommStats {
        std::chrono::steady_clock::time_point lastMessageTime;
        std::vector<std::chrono::milliseconds> rtt;

        double getAverageRTT() const
        {
            if (rtt.empty())
            {
                return 0.0;
            }
            double sum = std::accumulate(rtt.begin(), rtt.end(), 0.0,
                                         [](double acc, std::chrono::milliseconds rt)
                                         {
                                             return acc + rt.count();
                                         });
            return sum / rtt.size();
        }
    };

    int sockfd;
    int comm_port;
    struct sockaddr_in server_addr;

    std::atomic<bool> running;
    std::mutex bots_mutex;

    std::unordered_map<std::string, BotInfo> bots;
    std::unordered_map<std::string, CommStats> commStats;
    
    int next_bot_id;

    int messageStep;
    std::chrono::steady_clock::time_point lastResetTime;
    
    std::thread update_thread;

    std::string local_ip;

    void update();
    void listen();
    void handleBot(const struct sockaddr_in& bot_addr, const std::string& message);
    void handleAcknowledgement(const std::string& message, const struct sockaddr_in& bot_addr);
    std::string getBotKey(const struct sockaddr_in& bot_addr);
    void sendMessageToBot(const std::string& message, const struct sockaddr_in& bot_addr);
    std::string getLocalIPAddress();
};

#endif // UDPSERVER_HPP
