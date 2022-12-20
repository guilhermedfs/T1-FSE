#include <iostream>
#include <wiringPi.h>
#include <unistd.h>
#include <vector>
#include <chrono>
#include <thread>

#include "jsonConfig.hpp"
#include "socket.hpp"
#include "gpioUtil.hpp"
#include "dht22.hpp"

using namespace std;

static JsonConfig *jsonConfig;
int csock = -1;

void loop(chrono::milliseconds waitTime, void (*function)());
void readDHT22();
void handleSocket();

PI_THREAD(dht22Thread){
    loop(chrono::milliseconds(1000), &readDHT22);
    return NULL;
}

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        cout << "Necessário indicar arquivo JSON" << argv[0] << "<arquivo.json>" << endl << endl;
        return EXIT_SUCCESS;
    }

    if(wiringPiSetup() == -1)
    {
        cout << "Não foi possível iniciar o wiringPi" << endl;
    }

    try
    {
        jsonConfig = new JsonConfig(argv[1]);
        csock = sock::createSocket(
            jsonConfig->getIpCentralServer(),
            jsonConfig->getPortCentralServer(),
            jsonConfig->getName()
        );
        
        std::cout << "Aguardando conexão com o servidor." << std::endl;
        while (csock == -1)
        {
            csock = sock::createSocket(
                jsonConfig->getIpCentralServer(),
                jsonConfig->getPortCentralServer(),
                jsonConfig->getName()
            );
        }

        std::system("clear");
        cout << "Conectado em: " << jsonConfig->getIpCentralServer() << ":" << jsonConfig->getPortCentralServer() << endl; 

        gpio::input::set(csock);
        for(auto input : jsonConfig->getInputs())
            gpio::input::init(jsonConfig->getInput(input.getGpio()));
        
        bool sendCount = false;
        for(auto input : jsonConfig->getInputs()){
            usleep(10000);
            if(input.getType() == "contagem"){
                if(sendCount)
                    continue;
                else
                    sendCount = true;
            }
            sock::writeIoSocket(csock, input, sock::MODE_CREATE);
        }

        for(auto output : jsonConfig->getOutputs()){
            usleep(10000);
            sock::writeIoSocket(csock, output, sock::MODE_CREATE);
            gpio::output::init(output.getWPi());
        }

    } catch(JsonConfigException &e) {
        cout << e.what() << endl;
    } catch(sock::SocketException &e) {
        cout << e.what() << endl;
    }

    if (piThreadCreate(dht22Thread))
    {
        cout << "Falha ao criar as threads necessárias para o servico!" << endl;
        return EXIT_FAILURE;
    }

    while (true)
    {
        handleSocket();
    }

    delete jsonConfig;
    return EXIT_SUCCESS;
}

void handleSocket() 
{
    sleep(1);
    string msg = sock::readSocket(csock);
    gpio::output::set(msg);
}

void loop(chrono::milliseconds waitTime, void (*function)())
{
    chrono::milliseconds wait;
    chrono::high_resolution_clock::time_point startTime;
    chrono::high_resolution_clock::time_point endTime = chrono::high_resolution_clock::now();

    while (true)
    {
        startTime = chrono::high_resolution_clock::now();
        wait = chrono::duration_cast<chrono::milliseconds>(wait + waitTime - (startTime - endTime));

        function();

        if (wait.count() > 01)
        {
            std::this_thread::sleep_for(wait);
            wait = chrono::milliseconds(0);
        }
        endTime = chrono::high_resolution_clock::now();
    }
}

void readDHT22() {
    jsonConfig->getTemperatureSensor()->read();
    sock::writeDhtSocket(csock, *(jsonConfig->getTemperatureSensor()));
}