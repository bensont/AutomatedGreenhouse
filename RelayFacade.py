import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False) # disable warnings for now

Pins = [5,6,13,26]

# example to turn on and off
#for i in Pins:
#    GPIO.setup(i,GPIO.OUT)
#    GPIO.output(i, False)
#
#for i in Pins:
#    print("Setting pin", i, "to true.")
#    GPIO.output(i, True) # turn each relay on
#    sleep(3) # wait long enough to check that the output changed and the relay gets turned on
#    print("Setting pin", i, "to false.")
#    GPIO.output(i, False)
    
GPIO.setup(26, GPIO.OUT)
print("Setting pin 26 to false.")
GPIO.output(26, False)
sleep(2)
print("Setting pin 26 to true.")
GPIO.output(26, True)
sleep(10)
print("Setting pin 26 to false.")
GPIO.output(26, False)

#    
#class RelayFacade:
#    def __init__(self):
#        self.R1_on = Relay.On_Relay1()
#        self.R2_on = Relay.On_Relay2()
#        self.R3_on = Relay.On_Relay3()
#        self.R4_on = Relay.On_Relay4()
#        
#        self.R1_off = Relay.Off_Relay1()
#        self.R2_off = Relay.Off_Relay2()
#        self.R3_off = Relay.Off_Relay3()
#        self.R4_off = Relay.Off_Relay4()
#        
#
#class Relay:
#    def __init__(self):
#        self.relay1 = 5
#        self.relay2 = 6
#        self.relay3 = 13
#        self.relay4 = 26
#        
#    def On_Relay1:
#        GPIO.output(self.relay1,True)
#        print("Turned ON Relay 1")
#        
#    def On_Relay2:
#        GPIO.output(self.relay2,True)
#        print("Turned ON Relay 2")
#        
#    def On_Relay3:
#        GPIO.output(self.relay3,True)
#        print("Turned ON Relay 3")
#        
#    def On_Relay4:
#        GPIO.output(self.relay4,True)
#        print("Turned ON Relay 4")
#        
#    def Off_Relay1:
#        GPIO.output(self.relay1,False)
#        print("Turned ON Relay 1")
#        
#    def Off_Relay2:
#        GPIO.output(self.relay2,False)
#        print("Turned ON Relay 2")
#        
#    def Off_Relay3:
#        GPIO.output(self.relay3,False)
#        print("Turned ON Relay 3")
#        
#    def Off_Relay4:
#        GPIO.output(self.relay4,False)
#        print("Turned ON Relay 4")