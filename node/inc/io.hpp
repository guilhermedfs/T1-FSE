#ifndef IO_HPP_
#define IO_HPP_

#include <string>

class IO {

private:
    std::string type;
    std::string tag;
    int gpio;
    int value;
    int wPi;

public:
    IO(std::string type, std::string tag, int gpio, int wPi, int value);
    ~IO();

    std::string getType();
    std::string getTag();
    int getGpio();
    int getWPi();
    int getValue();

    void setValue(int value);

};


#endif