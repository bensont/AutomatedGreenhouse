# Light
import time
import tsl2591

# Temp/Humidity
import sys
import Adafruit_DHT

# Soil Temp/Humidity
from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw

# Facade to handle the sensor classes
class SensorFacade:
    # initialize needed values for communication with the sensor classes
    def __init__(self):
        self.light = LightSensor()
        self.air = AirSensor()
        self.soil = SoilSensor()

    # Get readings from all the sensors
    def get_readings(self):
        lux = self.light.get_lux()
        full = self.light.get_full()
        ir = self.light.get_ir()
        humidity = self.air.get_humidity()
        airTemp = self.air.get_temperature()
        moisture = self.soil.get_moisture()
        soilTemp = self.soil.get_temperature()

#        return lux,full, ir, humidity, airTemp, moisture, soilTemp
        return lux, full, ir, humidity, airTemp, moisture, soilTemp


# Light Sensor
class LightSensor:
    #tsl = tsl2591.Tsl2591()
    # initialize needed values for communication
    def __init__(self):
        self.tsl = tsl2591.Tsl2591()

    # get the lumin reading
    def get_lux(self):
        #tsl = tsl2591.Tsl2591()
        full, ir = self.tsl.get_full_luminosity()
        lux = self.tsl.calculate_lux(full, ir)
        print("Lux Reading:", lux)
        return lux

    # get the full reading
    def get_full(self):
        #tsl = tsl2591.Tsl2591()
        full, ir = self.tsl.get_full_luminosity()
        print("Full Reading:", full)
        return full

    # get the infra-red reading
    def get_ir(self):
        #tsl = tsl2591.Tsl2591()
        full, ir = self.tsl.get_full_luminosity()
        print("Infra-Red Reading", ir)
        return ir

# Temp/Humidity Sensor
class AirSensor:
#    sensor = Adafruit_DHT.DHT22
#    pin = 4
    # initialize needed values for communication
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT22
        self.pin = 4

    # get the air humidity from the sensor
    def get_humidity(self):
        #sensor = Adafruit_DHT.DHT22
        #pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        # Check that a reading was received
        if humidity is not None and temperature is not None:
            print("Humidity Reading:")
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return humidity

    # get the air temerature from the sensor
    def get_temperature(self):
        #sensor = Adafruit_DHT.DHT22
        #pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        # Check that a reading was received
        if humidity is not None and temperature is not None:
            print("Temperature Reading:")
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return temperature

# Soil Temp/Humidity Sensor
class SoilSensor:
    # initialize needed values for communication
    def __init__(self):
        self.i2c_bus = busio.I2C(SCL, SDA)
        # Need to put the address into the sensor constructor for each
        self.ss = Seesaw(self.i2c_bus, addr=0x36)

    # get the soil moisture from the sensor
    def get_moisture(self):
        #i2c_bus = busio.I2C(SCL, SDA)
        # Need to put the address into the sensor constructor for each
        #ss = Seesaw(i2c_bus, addr=0x36)
        # read moisture level through capacitive touch pad
        moisture = self.ss.moisture_read()
        print("Soil Moisture Reading:", moisture)
        return moisture

    # get the soil temperature from the sensor
    def get_temperature(self):
        #i2c_bus = busio.I2C(SCL, SDA)
        # Need to put the address into the sensor constructor for each
        #ss = Seesaw(i2c_bus, addr=0x36)
        # read temperature from the temperature sensor
        temp = self.ss.get_temp()
        print("Soil Temperatured Reading:", temp)
        return temp

# Added a main to test the facade independently
# def main():
#     sensorFacade = SensorFacade()
# #    lux,full, ir, humidity, airTemp, moisture, soilTemp = sensorFacade.get_readings()
# #    print("Light:", full, "Air Humidity:", humidity, "Air Temperature:", airTemp, "Soil Moisture:", moisture, "Soil Temperature:", soilTemp)
#     lux, full, ir, humidity, airTemp, moisture, soilTemp = sensorFacade.get_readings()
# #    print("Air Humidity:", humidity, "Air Temperature:", airTemp, "Soil Moisture:", moisture, "Soil Temperature:", soilTemp)
#     print()
#     print("Light (Full):", full, "Light (Lux):", lux, "Light (IR)", ir)
#     print("Air humidity:", humidity, "Air Temperature:", airTemp)
#     print("Soil Moisture:", moisture, "Soil Temperature:", soilTemp)
#
#
# if __name__ == "__main__":
#     main()
