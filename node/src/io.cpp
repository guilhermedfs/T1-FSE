#include "io.hpp"

IO::IO(std::string type, std::string tag, int gpio, int wPi, int value){
    this->type = type;
    this->tag = tag;
    this->gpio = gpio;
    this->wPi = wPi;
    this->value = value;
}

IO::~IO(){}

std::string IO::getType(){
    return type;
}

std::string IO::getTag(){
    return tag;
}

int IO::getGpio(){
    return gpio;
}

int IO::getWPi(){
    return wPi;
}

int IO::getValue(){
    return value;
}

void IO::setValue(int value){
    this->value = value;
}