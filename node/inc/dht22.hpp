#ifndef DHT22_HPP_
#define DHT22_HPP_

#include <string>

class DHT22 {

private:
    std::string type;
    std::string tag;
    int gpio;
    int wPi;
    float temperature;
    float humidity;

public:
    DHT22(std::string type, std::string tag, int gpio, int wPi);
    ~DHT22();

    std::string getType();
    std::string getTag();
    int getGpio();
    int getWPi();
    float getTemperature();
    float getHumidity();

    void read();

};

#endif