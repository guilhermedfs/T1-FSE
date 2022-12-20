#include "dht22.hpp"
#include <wiringPi.h>


static int values[5] = {0, 0, 0, 0, 0};
static float lastTemperature = -1;
static float lastHumidity = -1;


static const long WAIT_TIME = 1;
static const long MAX_TIMINGS = 85;


DHT22::DHT22(std::string type, std::string tag, int gpio, int wPi){
	this->type = type;
	this->tag = tag;
	this->gpio = gpio;
	this->wPi = wPi;
	this->temperature = 0;
	this->humidity = 0;
}

DHT22::~DHT22(){}

std::string DHT22::getType(){
	return type;
}

std::string DHT22::getTag(){
	return tag;
}

int DHT22::getGpio(){
	return gpio;
}

int DHT22::getWPi(){
	return wPi;
}

float DHT22::getTemperature(){
	return temperature;
}

float DHT22::getHumidity(){
	return humidity;
}

void DHT22::read(){
	unsigned char laststate = HIGH;
	unsigned char counter	= 0;
	unsigned char j = 0;
	unsigned char i;

	values[0] = values[1] = values[2] = values[3] = values[4] = 0;

	pinMode(wPi, OUTPUT);
	digitalWrite(wPi, LOW);
	delay(18);
	pinMode(wPi, INPUT);

	for(i = 0; i < MAX_TIMINGS; i++){
		counter = 0;
		while(digitalRead(wPi) == laststate){
			counter++;
			delayMicroseconds(1);
			if(counter == 255)
				break;
		}
		laststate = digitalRead(wPi);

		if(counter == 255)
			break;

		if((i >= 4) && (i % 2 == 0)){
			values[j / 8] <<= 1;
			if ( counter > 16 )
				values[j / 8] |= 1;
			j++;
		}
	}

	if((j >= 40) && (values[4] == ( (values[0] + values[1] + values[2] + values[3]) & 0xFF))){

		float h = (float)((values[0] << 8) + values[1]) / 10;
		if(h > 100)
			h = values[0];
		
		float c = (float)(((values[2] & 0x7F) << 8) + values[3]) / 10;
		if(c > 125)
			c = values[2];

		if(values[2] & 0x80)
			c = -c;

		lastTemperature = temperature = c;
		lastHumidity = humidity = h;
	}else{
		temperature = lastTemperature;
		humidity = lastHumidity;
	}
}