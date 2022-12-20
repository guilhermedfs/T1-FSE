#ifndef ISR_FUNCTIONS_H_
#define ISR_FUNCTIONS_H_


#include "io.hpp"
#include <string>


namespace gpio {

    namespace input {

        void set(int sock_);
        void init(IO *input);

    }

    namespace output {

        void init(int wpi);
        void set(std::string gpio_value);

    }
}


#endif