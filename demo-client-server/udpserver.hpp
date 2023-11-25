#ifndef UDPSERVER_HPP
#define UDPSERVER_HPP

#include <atomic>
#include <thread>
#include <mutex>
#include <netinet/in.h>

class UdpServer {
public:
    UdpServer(int port);
    ~UdpServer();

    void start();
    void stop();

private:
    int sockfd;
    struct sockaddr_in server_addr;
    std::atomic<bool> running;
    std::mutex mutex;

    void listen();
};

#endif // UDPSERVER_HPP

