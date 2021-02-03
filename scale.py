from hx711 import HX711
from utime import sleep

class Scales(HX711):
    """
    An extension for  SergeyPiskunov's HX711 library
    (https://github.com/SergeyPiskunov/micropython-hx711)
    
    Most of the fuctions were taken from bogde's Arduino HX711 driver
    (https://github.com/bogde/HX711)
    and rewritten to micropython
    """
    
    def __init__(self, d_out, pd_sck, channel=HX711.CHANNEL_A_128):
        # Setup an HX711 board
        # wiring:
        # DT to pin d_out
        # sck to pin pd_sck 
        super().__init__(d_out, pd_sck, channel)
        self.OFFSET = 0 
        self.SCALE = 1
        # reset sensor value offset and scale
    
    def reset(self):
        self.power_off()
        self.power_on()
        # reboot sensor
    
    def tare(self, numReadings=1, howLong = 0):
        avg = self.avgRead(num=numReadings, interval=howLong)
        # get mean value over specified time and number of readings
        self.setOffset(avg)
        # and make it the offset
    
    def readUnits(self, numReadings=1, howLong = 0):
        return (self.avgRead(num=numReadings, interval=howLong) - self.OFFSET)/self.SCALE
        # return sensor value, converted to your unit of choice
        # the equation is (raw_reading - offset)/scale 

    def avgRead(self, num=1, interval=0):
        readingSum = 0
        delay = interval / num
        # specify number of tries and total measurement time
        for i in range(num):
            readingSum += self.read()
            sleep(delay)
        return readingSum/num
        # return the mean value

    def setOffset(self, offset=0):
        self.OFFSET = offset

    def setScale(self, scale=1):
        self.SCALE = scale
