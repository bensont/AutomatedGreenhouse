import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # disable warnings for now

Pins = [5,6,13,26]


class RelayFacade:
    def __init__(self):
        self.relay1 = Pins[0]
        self.relay2 = Pins[1]
        self.relay3 = Pins[2]
        self.relay4 = Pins[3]
        AllOff()
        
    def AllOff(self):
        #this could be changed to a set of function calls, but on a small machine isn't worth it
        GPIO.output(self.relay1, True)
        GPIO.output(self.relay2, True)
        GPIO.output(self.relay3, True)
        GPIO.output(self.relay4, True)
        
    def AllOn(self):
        GPIO.output(self.relay1, False)
        GPIO.output(self.relay2, False)
        GPIO.output(self.relay3, False)
        GPIO.output(self.relay4, False)
        
    def RelayNOn(self,relaynum):
        GPIO.output(NumToRelay(relaynum),False)
        
    def RelayNOff(self,relaynum):
        GPIO.output(NumToRelay(relaynum),True)
        
    def NumToRelay(self,relaynum):
        if(relaynum == 1):
            return self.relay1
        elif(relaynum == 2):
            return self.relay2
        elif(relaynum == 3):
            return self.relay3
        elif(relaynum == 4):
            return self.relay4
        
        #if we fall through probably throw an exception?