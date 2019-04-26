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
plot using the relay facade.
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
* Air Temperature/Humidity Sensor (https://www.adafruit.com/product/393)
* Soil Temperature/Moisture Sensor (https://www.adafruit.com/product/4026)
* Light Sensor (https://www.adafruit.com/product/1980)
* Raspberry Pi Camera (https://www.adafruit.com/product/3099)
* Grow Light
* Water pump
* Ceramic Heater
* Humidifier
* Relay (https://www.amazon.com/JBtek-Channel-Module-Arduino-Raspberry/dp/B00KTEN3TM)
* 5 V power source (to power relay instead of powering via the RPi, safety...)
* Breadboard
* Jumper wires

Note: Make sure that the grow light, water pump, heater, and humidifier all are
within specs for the relay. The relay used in this project can handle 10 A across
each relay at 110 V. BE CAREFUL WITH POWER! Check the Ohms across all connections
before connecting 110 V AC power. For safety, we used a 24 V DC power source to check all
connections first. Follow the wiring diagrams provided in the links for each device.
<br/>
<br/>
When wiring power distribution, it is recommended to use a GFI between the relay and
the wall. This will ensure that the components are safe in the event of a power surge
and prevents the low-voltage on relay board allowing power to devices in the event
of the RPi shutting down due to a momentary power loss. Tie all common on each relay
together and run power from the normally open relay position on each relay to a different
outlet. We used a box with four outlet sockets as to power each of the four environment
devices. Run grounds accordingly and connect power to one side of each outlet. If this
is done correctly, checking the ohm reading across the relays should change as the relays
switch going from infinite to 0. If the readings are good, check the same ohm reading
through the sockets to ensure wiring has been done correctly.
<br/>
<br/>
PLEASE BE CAREFUL WITH A/C POWER. It is dangerous and if you aren't comfortable
doing the wiring, please consult your local electrician. Remember to cover all wires
to prevent arcing and grounding. Be smart. Be aware.
<br/>
<br/>
With the wiring done, run ground from the power supply to the relay ground and
run 5 volts to the relay power pin. Keep the jumper on the board IN. Connect relay
pins to desired GPIO pins (we used 5, 6, 13, and 26). Consult a RPi pinout online
for GPIO pin locations.
<br/>
<br/>
DO NOT POWER WITH A/C CURRENT UNTIL ALL WIRING IS DONE AND INSTALLATION IS COMPLETE.
When all is done, plug environment devices (humidifier, water pump, etc.) to the
power outlets and plug the 5 v power converter and RPi into the GFI outlet.
<br/>
<br/>
Plug the GFI into power and have fun!

## Installation
***
There are several steps necessary to get the libraries needed to run the system.
First get python 3 and git installed if they aren't already on the Raspberry Pi.
You will also need the matplotlib library.
<br/>
<br/>
sudo pip3 install matplotlib
***
### DHT22 Temperature/Humidity Sensor
sudo apt-get update
<br/>
<br/>
sudo apt-get install build-essential python-dev python-openssl git
<br/>
<br/>
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
<br/>
<br/>
sudo python setup.py install
<br/>
<br/>
sudo pip3 install Adafruit_DHT
***
For detailed installation and wiring guide:
https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
<br/>
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
<br/>
python3 setup.py install
***
See the GitHub repository provided by user maxlklaxl for questions with the module
and some simple example code. **Credit to GitHub user maxlklaxl for this library.** We had trouble
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
<br/>
open browser to localhost:36636
***
