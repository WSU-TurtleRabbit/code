#ifndef UDPCLIENT_HPP
#define UDPCLIENT_HPP

#include <string>
#include <netinet/in.h>

class UdpClient {
public:
    UdpClient(const std::string& server_ip, int server_port);
    ~UdpClient();

    void sendMessage(const std::string& message);
    std::string receiveMessage();
    std::string listenForBroadcast(int broadcastPort);
    void setServerAddress(const std::string& server_ip, int server_port);

private:
    int sockfd;
    struct sockaddr_in server_addr;
};

#endif // UDPCLIENT_HPP

