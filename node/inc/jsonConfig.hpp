#ifndef JSON_CONFIG_HPP_
#define JSON_CONFIG_HPP_

#include "io.hpp"
#include "dht22.hpp"

#include <string>
#include <vector>
#include <exception>

class JsonConfigException : public std::exception {

private:
    std::string userMessage;

public:
    JsonConfigException(const std::string message) throw();
    ~JsonConfigException() throw();

    const char *what() const throw();

};

class JsonConfig {

private:
    std::string name;
    std::string ipCentralServer;
    int portCentralServer;
    std::string ipDistributedServer;
    int portDistributedServer;
    std::vector<IO> outputs;
    std::vector<IO> inputs;
    DHT22 *temperatureSensor;

public:
    JsonConfig(std::string json_path);
    ~JsonConfig();

    std::string getName();
    std::string getIpCentralServer();
    int getPortCentralServer();
    std::string getIpDistributedServer();
    int getPortDistributedServer();
    IO* getOutput(int gpio);
    IO* getInput(int gpio);
    std::vector<IO> getOutputs();
    std::vector<IO> getInputs();
    DHT22* getTemperatureSensor();

};

#endif