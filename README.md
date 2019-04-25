# Automated Greenhouse
Tyler Benson, Tyler Mooney, Benjamin Goldstein
***
## Overview:
This project provides code and information for building an indoor automated greenhouse.
Some basic equipment is needed as well as some basic electrical knowledge. Once running,
the greenhouse monitors air moisture and humidity, soil moisture and temperature, and
light in accordance to the ideal plant information stored using a MySQL database (MariaDB).
A local web app runs in parallel showing the most recent data, the most recent photo
taken of the plant, and graphs tracking important environment data for the plant. This
simple interface allows the user to easily interpret the environment data in order
to make informed changes to the plant environment requirements. The system uses the
plant requirements (also stored in the database) to turn on/off a heater, a grow
light, a water pump, and a humidifier in order to maintain an ideal environment.

## Files
* CameraFacade.py - Facade and camera class to take photos of the plant. Only one
Pi camera can be used. To add more, assign to the USB ports and use webcams.
* DatabaseConnection.py - Sets up the database and handles database calls
* Main.py - Sets up the plot for a plant and continually monitors environment
conditions through the plot using sensor facade and changes the environment through the
plot using relay facade.
* Plot.py - Plot object containing a plant. Monitors its condition and changes
the environment accordingly through the use of the sensor facade and relay facade.
* RelayFacade.py - Handles turning on/off the different devices. More relays can
be added using more GPIO pins. This can easily be modified to handle this through
implementing the facade, but for basic purposes, just a basic class is implemented
to run a single relay.
* SensorFacade.py - Contains facade for handling the different sensors and classes
for each sensor to get and return readings.
* webapp.py - Contains the web app to view data in the database regarding the plant

## Project components
* Raspberry Pi
* Air Temperature/Humidity Sensor
* Soil Temperature/Moisture Sensor
* Light Sensor
* Raspberry Pi Camera
* Grow Light
* Water pump
* Ceramic Heater
* Humidifier
* Relay
* 5 V power source (to power relay instead of powering via the RPi, safety...)
* Breadboard
* Jumper wires

Note: Make sure that the grow light, water pump, heater, and humidifier all are
within specs for the relay. The relay used in this project can handle 10 A across
each relay at 110 V. BE CAREFUL WITH POWER! Check the Ohms across all connections
before connecting 110 V AC power. For safety, we used a 24 V DC power source to check all
connections first.

## Installation
***
There are several steps necessary to get the libraries needed to run the system.
First get python 3 and git installed if they aren't already on the Raspberry Pi.
You will also need the matplotlib library.
<br/>
sudo pip3 install matplotlib
***
### DHT22 Temperature/Humidity Sensor
sudo apt-get update
<br/>
sudo apt-get install build-essential python-dev python-openssl git
<br/>
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
<br/>
sudo python setup.py install
<br/>
sudo pip3 install Adafruit_DHT
***
For detailed installation and wiring guide:
https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
<br/>
If you are interested in how the sensor works, you can now look through the
downloaded repository for examples.
***
### STEMMA Soil Sensor
sudo pip3 install adafruit-circuitpython-seesaw
***
This sensor uses the I2C bus. For detailed Installation and a wiring guide:
https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/python-circuitpython-test
***
### TSL 2591 Light Sensor
***
git clone https://github.com/maxlklaxl/python-tsl2591.git
<br/>
python3 setup.py install
***
See the GitHub repository provided by user maxlklaxl for questions with the module
and some simple example code. Credit to maxlklaxl for this library. We had trouble
using the standard Adafruit module for the sensor.
***
This sensor uses the I2C bus. For further information on the TSL2591 and the wiring guide:
https://learn.adafruit.com/adafruit-tsl2591/python-circuitpython
***
### Download Repository
***
git clone https://github.com/bensont/AutomatedGreenhouse.git
***
### Execute
***
python3 Main.py
<br/>
open browser to localhost::36636
***
