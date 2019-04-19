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


class SensorFacade:
    def __init__(self):
        self.light = LightSensor()
        self.air = AirSensor()
        self.soil = SoilSensor()
        
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
    def get_lux(self):
        tsl = tsl2591.Tsl2591()
        full, ir = tsl.get_full_luminosity()
        lux = tsl.calculate_lux(full, ir)
        print("Lux Reading:", lux)
        return lux
        
    def get_full(self):
        tsl = tsl2591.Tsl2591()
        full, ir = tsl.get_full_luminosity()
        print("Full Reading:", full)
        return full
    
    def get_ir(self):
        tsl = tsl2591.Tsl2591()
        full, ir = tsl.get_full_luminosity()
        print("Infra-Red Reading", ir)
        return ir

# Temp/Humidity Sensor
class AirSensor:
#    sensor = Adafruit_DHT.DHT22
#    pin = 4
    
    def get_humidity(self):
        sensor = Adafruit_DHT.DHT22
        pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            print("Humidity Reading:")
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return humidity
    
    def get_temperature(self):
        sensor = Adafruit_DHT.DHT22
        pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            print("Temperature Reading:")
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return humidity
#    
## Soil Temp/Humidity Sensor
class SoilSensor:
    i2c_bus = busio.I2C(SCL, SDA)
    # Need to put the address into the sensor constructor for each
    ss = Seesaw(i2c_bus, addr=0x36)

    def get_moisture(self):
        i2c_bus = busio.I2C(SCL, SDA)
        # Need to put the address into the sensor constructor for each
        ss = Seesaw(i2c_bus, addr=0x36)
        # read moisture level through capacitive touch pad
        moisture = ss.moisture_read()
        print("Soil Moisture Reading:", moisture)
        return moisture
    
    def get_temperature(self):
        i2c_bus = busio.I2C(SCL, SDA)
        # Need to put the address into the sensor constructor for each
        ss = Seesaw(i2c_bus, addr=0x36)
        # read temperature from the temperature sensor
        temp = ss.get_temp()
        print("Soil Temperatured Reading:", temp)
        return temp

# Added a main to test the facade independently
def main():
    sensorFacade = SensorFacade()
#    lux,full, ir, humidity, airTemp, moisture, soilTemp = sensorFacade.get_readings()
#    print("Light:", full, "Air Humidity:", humidity, "Air Temperature:", airTemp, "Soil Moisture:", moisture, "Soil Temperature:", soilTemp)
    lux, full, ir, humidity, airTemp, moisture, soilTemp = sensorFacade.get_readings()
#    print("Air Humidity:", humidity, "Air Temperature:", airTemp, "Soil Moisture:", moisture, "Soil Temperature:", soilTemp)
    print()
    print("Light (Full):", full, "Light (Lux):", lux, "Light (IR)", ir)
    print("Air humidity:", humidity, "Air Temperature:", airTemp)
    print("Soil Moisture:", moisture, "Soil Temperature:", soilTemp)


if __name__ == "__main__":
    main()
