import SensorFacade
import RelayFacade
import CameraFacade

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
        self.humidity_min = info[3]
        self.humidity_max = info[4]
        self.temperature_min = info[5]
        self.temperature_max = info[6]
        self.water_seconds = info[7]
        self.water_interval = info[8]
        self.moisture_min = info[9]
        self.moisture_max = info[10]
       
        #these will both need to be transitioned into Dependancy Injection
        self.sensor_facade = SensorFacade.SensorFacade()
        #when we add more than one plot, this is illigal
        self.relay_facade = RelayFacade.RelayFacade()
        self.camera_facade = CameraFacade.CameraFacade()
        
        # Information for the GPIO for each device on the relay
        #self.light_GPIO = light_GPIO
        #self.humidifier_GPIO = humidifier_GPIO
        #self.heater_GPIO = heater_GPIO
        #self.water_GPIO = water_GPIO
        

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
            print("Turn on HEATER")
        if self.cur_airTemp > self.temperature_max:
            # potentially turn on heater
            self.relay_facade.RelayNOff(1)
            print("Turn off HEATER")
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
        check_watering()
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

    def check_watering(self):
        #Needs to make a daemon thread to turn of waterer after n seconds
        if self.cur_moisture < self.moisture_min:
            # potentially turn on water pump (send seconds to be turned on)
            # there needs to be a check to see when the last time the plot was watered. If too recently, don't water
            self.relay_facade.RelayNOn(3)
            print("Turn on WATER")

    def return_current(self):
        return (self.cur_light_lux, self.cur_light_full, self.cur_light_ir, self.cur_humidity, self.cur_airTemp, self.cur_moisture, self.cur_soilTemp)