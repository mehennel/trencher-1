import pigpio #importing GPIO library
import time

class HallEffectSensor(Sensor):
    __pin = None
    __pi = None
    __revolutions = None
    __currRevs = None
    __rpms = None
    __startTime = None

    def __init__(self, pi, pin, revolutions):
        self.__pi = pi
        self.__pin = pin
        self.__pi.set_mode(pin, pigpio.INPUT)
        self.__revolutions = revolutions
        self.__rpms = 0
        self.__currRevs = 0
        self.__startTime = time.time()

    def read(self):
        return self.__pi.read(pin)

    def measureRPMs(self):
        # Called if sensor output changes
        if (self.read() == 0):
            self.__currRevs += 1

        if (self.__currRevs == self.__revolutions + 1): #plus 1 means it went full circle
            rpmEndTime = time.time()
            rpmDelta = (rpmEndTime - self.__startTime)
            self.__startTime = time.time()
            self.__rpms = 1.0 / ((rpmDelta) / 60.0)
            self.__currRevs = 0

        return self.__rpms
