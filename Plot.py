import SensorFacade

class Plot(object):
    def __init__(self, name, category, light_minutes, light_min, humidity_min, humidity_max, moisture_min, moisture_max, water_seconds, water_interval, notes, cur_airTemp = None, cur_humidity = None, cur_moisture = None, cur_soilTemp = None, cur_light_full = None, cur_light_ir = None, cur_light_lux = None):
        #This should be requested from the database rather than passed in
        # Semi-Permanent variables. Can be changed in the database
        self.name = name
        self.category = category
        self.light_minutes = light_minutes
        self.light_min = light_min
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max
        #self.temperature_min = temperature_min
        #self.temperature_max = temperature_max
        self.moisture_min = moisture_min
        self.moisture_max = moisture_max
        self.water_seconds = water_seconds # this could be done in ounces, but this is easier for the pump, which has its own adjustment knob for flow rate
        self.water_interval = water_interval # this is done in DAYS
        self.notes = notes
        # Sensor variables for the most recent sensor information
        self.cur_airTemp = cur_airTemp
        self.cur_humidity = cur_humidity
        self.cur_moisture = cur_moisture
        self.cur_soilTemp = cur_soilTemp
        self.cur_light_full = cur_light_full
        self.cur_light_ir = cur_light_ir
        self.cur_light_lux = cur_light_lux
        # Information for the GPIO for each device on the relay
        #self.light_GPIO = light_GPIO
        #self.humidifier_GPIO = humidifier_GPIO
        #self.heater_GPIO = heater_GPIO
        #self.water_GPIO = water_GPIO
        self.sensor_facade = SensorFacade.SensorFacade()

    # Function uses the sensor facade to get the current sensor readings for the plot
    def get_condition(self):
        self.cur_light_lux, self.cur_light_full, self.cur_light_ir, self.cur_humidity, self.cur_airTemp, self.cur_moisture, self.cur_soilTemp = self.sensor_facade.get_readings()
        # Check for potential read errors

    # Function checks its current condition to see if any devices need turned on/off to adjust the environment
    def check_condition(self):
        # Check air temperature
        if self.cur_airTemp < self.temperature_min:
            # potentially turn on heater
            print("Turn on HEATER")
        # Check air humidity
        if self.cur_humidity < self.humidity_min:
            # potentially turn ON humidifier
            print("Turn on HUMIDIFIER")
        if self.cur_humidity >= self.humidity_max:
            # potentially turn OFF humidifier
            print("Turn off HUMIDIFIER")
        # Check soil moisture
        if self.cur_moisture < self.moisture_min:
            # potentially turn on water pump (send seconds to be turned on)
            print("Turn on WATER")
        # Check light (use full)
        if self.cur_light_full < self.light_min:
            # potentially turn on light
            print("Turn on LIGHT")


    def return_current(self):
        return (self.cur_light_lux, self.cur_light_full, self.cur_light_ir, self.cur_humidity, self.cur_airTemp, self.cur_moisture, self.cur_soilTemp)