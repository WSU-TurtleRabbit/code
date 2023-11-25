#ifndef UDPCLIENT_HPP
#define UDPCLIENT_HPP

#include <string>
#include <netinet/in.h>

class UdpClient {
public:
    UdpClient(const std::string& server_ip, int server_port);
    ~UdpClient();

    void sendMessage(const std::string& message);

private:
    int sockfd;
    struct sockaddr_in server_addr;
};

#endif // UDPCLIENT_HPP

