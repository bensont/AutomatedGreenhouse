import SensorFacade
import RelayFacade
import CameraFacade
import time
from time import sleep

class Plot(object):
    def __init__(self, indb, incv,inpnum):
        #call the database to ask about itself
        self.plant_num = inpnum
        #Some Dependancy Injection
        self.database = indb
        self.cv = incv
        info = []
        with self.cv:
            info = self.database.GetPlantInfo(inpnum)
        self.name = info[0]
        self.light_min = info[1]
        self.light_max = info[2]
        self.light_minutes = info[3]
        self.humidity_min = info[4]
        self.humidity_max = info[5]
        self.temperature_min = info[6] # switch to 5 after demo
        self.temperature_max = info[7] # switch to 6 after demo... inverted to show readings have actions
        self.water_seconds = info[8]
        self.water_interval = info[9]
        self.moisture_min = info[10]
        self.moisture_max = info[11]
        
        self.last_watered = time.time()
        
        # for debug purposes to make sure the passing happend correctly
        print("Name:" + self.name)
        print("Light Min:" + str(self.light_min))
        print("Light Max:" + str(self.light_max))
        print("light Minutes:" + str(self.light_minutes))
        print("Hum Min:" + str(self.humidity_min))
        print("Hum Max:" + str(self.humidity_max))
        print("Temp Max:" + str(self.temperature_max))
        print("Temp Min:" + str(self.temperature_min))
        print("Water Sec:" + str(self.water_seconds))
        print("Water Int:" + str(self.water_interval))
        print("Moist Min:" + str(self.moisture_min))
        print("Moist Max:" + str(self.moisture_max))

       
        #these will both need to be transitioned into Dependancy Injection
        self.sensor_facade = SensorFacade.SensorFacade()
        #when we add more than one plot, this is illigal
        self.relay_facade = RelayFacade.RelayFacade()
        self.camera_facade = CameraFacade.CameraFacade()
        

    # Function uses the sensor facade to get the current sensor readings for the plot
    def get_condition(self):
        self.cur_light_lux, self.cur_light_full, self.cur_light_ir, self.cur_humidity, self.cur_airTemp, self.cur_moisture, self.cur_soilTemp = self.sensor_facade.get_readings()
        # Check for potential read errors

    # Function checks its current condition to see if any devices need turned on/off to adjust the environment
    def check_condition(self):
        # Check air temperature
        if self.cur_airTemp < self.temperature_min:
            # potentially turn on heater
            self.relay_facade.RelayNOn(1)
            print("Turn on HEATER: cur temp:" + str(self.cur_airTemp) + " min temp:" + str(self.temperature_min))
        if self.cur_airTemp > self.temperature_max:
            # potentially turn on heater
            self.relay_facade.RelayNOff(1)
            print("Turn off HEATER: cur temp:" + str(self.cur_airTemp) + " max temp:" + str(self.temperature_max))
        # Check air humidity
        if self.cur_humidity < self.humidity_min:
            # potentially turn ON humidifier
            self.relay_facade.RelayNOn(2)
            print("Turn on HUMIDIFIER")
        if self.cur_humidity >= self.humidity_max:
            # potentially turn OFF humidifier
            self.relay_facade.RelayNOff(2)
            print("Turn off HUMIDIFIER")
        # Check soil moisture
        self.check_watering()
        # Check light (use full)
        if self.cur_light_full < self.light_min:
            # potentially turn on light
            # needs to check the time of day to see if the light should be on for the plot's light time window
            self.relay_facade.RelayNOn(4)
            print("Turn on LIGHT")
        if self.cur_light_full > self.light_max:
            # potentially turn on light
            # needs to check the time of day to see if the light should be on for the plot's light time window
            self.relay_facade.RelayNOff(4)
            print("Turn off LIGHT")
        # Check the time of day to turn the light off if the time is outside the plot's light time window

    # Helper function to check conditions for watering. If the plant has been watered too recently, don't water it.
    def check_watering(self):
        print("Checking Water Function: Cur Moisture:" + str(self.cur_moisture) + "Min Moisture" + str(self.moisture_min))
        # Needs to make a daemon thread to turn of waterer after n seconds this works, but the program is essentailly paused for watering
        # check if the moisture level is low AND the time since last watered is long enough for the plant guidelines
        if (self.cur_moisture < self.moisture_min) and ((time.time() - self.last_watered) > (self.water_interval * 86400)):
            # potentially turn on water pump
            # there needs to be a check to see when the last time the plot was watered. If too recently, don't water
            print("Turn on WATER")
            self.relay_facade.RelayNOn(3)
            sleep(self.water_seconds)
            self.relay_facade.RelayNOff(3)
            print("Turn off WATER")
            self.last_watered = time.time()

    def return_current(self):
        return (self.cur_light_lux, self.cur_light_full, self.cur_light_ir, self.cur_humidity, self.cur_airTemp, self.cur_moisture, self.cur_soilTemp)