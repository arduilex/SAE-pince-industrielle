import RPi.GPIO as GPIO
from time import time, sleep

class CapteurHC(object):
    def __init__(self, pins={"trig":26, "echo":19}):
        GPIO.setmode(GPIO.BCM)
        self.GPIO_TRIGGER = pins["trig"]
        self.GPIO_ECHO = pins["echo"]
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
    def get_timing(self, mode="beter"):
        timing = {"good":7, "beter":11, "best":21, "speed":1}
        self.n = timing[mode]
        return 0.05
    def get_mesure(self):
        """Fonction qui retourne la distance en mm que le capteur HCSR04 à mesurer via des ultrasons"""
        GPIO.output(self.GPIO_TRIGGER, True)
        sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)  
        StartTime=time()
        StopTime=time() 
        deltaTime=time()
        while GPIO.input(self.GPIO_ECHO) == 0 and time() - deltaTime<0.3:   
            StartTime=time() 
        while GPIO.input(self.GPIO_ECHO) == 1 and time() - deltaTime<0.3:
            StopTime=time() 
        TimeElapsed = StopTime - StartTime
        length = (TimeElapsed*343000)/2
        return length
    def get_distance(self):
        mesures = []
        for k in range(self.n):
            mesures.append(self.get_mesure())
        mesures.sort()
        return round(mesures[self.n//2])