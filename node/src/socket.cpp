#include "socket.hpp"
#include "cJSON.h"

#include <sys/socket.h>
#include <arpa/inet.h> //inet_addr
#include <unistd.h>    //write
#include <time.h>
#include <string.h>


const int BUFFSIZE = 256;


sock::SocketException::SocketException(const std::string message)
    throw() : userMessage(message){}

sock::SocketException::~SocketException() throw() {}

const char *sock::SocketException::what() const throw() {
    return userMessage.c_str();
}


void sock::closeSocket(int sock_fd){
    close(sock_fd);
}

int sock::createSocket(std::string ip, int port, std::string room){

    int sock;
    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    inet_pton(AF_INET, ip.c_str(), &server_address.sin_addr);

    if((sock = socket(PF_INET, SOCK_STREAM, 0)) < 0)
        return -1;

    if(connect(sock, (struct sockaddr*)&server_address, sizeof(server_address)) < 0)
        return -1;

    cJSON *json = cJSON_CreateObject();
    cJSON *mode = cJSON_CreateString(MODE_CREATE);
    cJSON *type = cJSON_CreateString("nome");
    cJSON *tag = cJSON_CreateString(room.c_str());
    cJSON *gpio = cJSON_CreateNumber(0);
    cJSON *value = cJSON_CreateNumber(0);

    if(json == NULL || mode == NULL || type == NULL || tag == NULL || gpio == NULL || value == NULL)
        throw SocketException("Não foi possível gerar mensagem para o host");

    cJSON_AddItemToObject(json, "mode", mode);
    cJSON_AddItemToObject(json, "type", type);
    cJSON_AddItemToObject(json, "tag", tag);
    cJSON_AddItemToObject(json, "gpio", gpio);
    cJSON_AddItemToObject(json, "value", value);

    std::string str_msg = cJSON_Print(json);

    if(send(sock, (void*)str_msg.c_str(), str_msg.size(), 0) < 0){
        close(sock);
        cJSON_Delete(json);
        throw SocketException("Não foi possível enviar mensagem inicial ao host");
    }

    cJSON_Delete(json);
    return sock;
}

void sock::writeIoSocket(int sock, IO io, const char* mode_){

    if(sock == -1) return;

    cJSON *json = cJSON_CreateObject();
    cJSON *mode = cJSON_CreateString(mode_);
    cJSON *type = cJSON_CreateString(io.getType().c_str());
    cJSON *tag = cJSON_CreateString(io.getTag().c_str());
    cJSON *gpio = cJSON_CreateNumber(io.getWPi());
    cJSON *value = cJSON_CreateNumber(io.getValue());
    
    if(json == NULL || mode == NULL || type == NULL || tag == NULL || gpio == NULL || value == NULL)
        throw SocketException("Não foi possível gerar mensagem para o host");

    cJSON_AddItemToObject(json, "mode", mode);
    cJSON_AddItemToObject(json, "type", type);
    cJSON_AddItemToObject(json, "tag", tag);
    cJSON_AddItemToObject(json, "gpio", gpio);
    cJSON_AddItemToObject(json, "value", value);

    std::string str_msg = cJSON_Print(json);

    if(send(sock, (void*)str_msg.c_str(), str_msg.size(), 0) < 0){
        close(sock);
        cJSON_Delete(json);
        throw SocketException("Não foi possível enviar mensagem para o host");
    }

    cJSON_Delete(json);
}

void sock::writeDhtSocket(int sock, DHT22 dht){

    if(sock == -1) return;

    cJSON *json = cJSON_CreateObject();
    cJSON *mode = cJSON_CreateString(MODE_UPDATE);
    cJSON *type = cJSON_CreateString(dht.getType().c_str());
    cJSON *tag = cJSON_CreateString(dht.getTag().c_str());
    cJSON *temperatura = cJSON_CreateNumber(dht.getTemperature());
    cJSON *humidade = cJSON_CreateNumber(dht.getHumidity());
    
    if(json == NULL || mode == NULL || type == NULL || tag == NULL || temperatura == NULL || humidade == NULL)
        throw SocketException("Não foi possível gerar mensagem para o host");

    cJSON_AddItemToObject(json, "mode", mode);
    cJSON_AddItemToObject(json, "type", type);
    cJSON_AddItemToObject(json, "tag", tag);
    cJSON_AddItemToObject(json, "temperatura", temperatura);
    cJSON_AddItemToObject(json, "humidade", humidade);

    std::string str_msg = cJSON_Print(json);

    if(send(sock, (void*)str_msg.c_str(), str_msg.size(), 0) < 0){
        close(sock);
        cJSON_Delete(json);
        throw SocketException("Não foi possível enviar mensagem para o host");
    }

    cJSON_Delete(json);
}

std::string sock::readSocket(int sock){

    char buff[BUFFSIZE];
    bzero(buff, BUFFSIZE);
    if(recv(sock, buff, BUFFSIZE, 0) <= 0) return "";
    return std::string(buff);
}