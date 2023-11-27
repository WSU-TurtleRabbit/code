#ifndef UDPCLIENT_HPP
#define UDPCLIENT_HPP

#include <atomic>
#include <string>
#include <vector>
#include <netinet/in.h>

class UdpClient {
public:
    UdpClient(const std::string& server_ip, int server_port);
    ~UdpClient();

    void sendMessage(const std::string& message) const;
    void sendInitialMessage() const;
    bool waitForTurtle(int timeOutMS);
    
    std::string receiveMessage();
    
    
    void setServerAddress(const std::string& server_ip, int server_port);

    void receiveUpdates();

private:
    std::atomic<bool> isConnected;
    
    int sockfd;
    struct sockaddr_in server_addr;
};

#endif // UDPCLIENT_HPP

