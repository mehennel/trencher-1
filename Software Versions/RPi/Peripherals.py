import pigpio #importing GPIO library
import time

class Motor():
    __dir = None
    __speed = None
    __pi = None
    __break = None
    __currSpeed = None

    def __init__(self, pi, sv, fr, brk):
        self.__pi = pi
        self.__speed = sv
        self.__dir = fr
        self.__break = brk
        self.__pi.set_mode(self.__dir, pigpio.OUTPUT)
        self.__pi.set_mode(self.__speed, pigpio.OUTPUT)
        self.__pi.set_mode(self.__break, pigpio.OUTPUT)
        self.__currSpeed = 0

    def setSpeed(self, speed):
        if speed > 255:
            self.__currSpeed = 255
        elif speed < 0:
            self.__currSpeed = 0
        else:
            self.__currSpeed = speed

        self.__pi.set_servo_pulsewidth(self.__speed, self.__currSpeed)

    def speedUp(self, amount):
        self.setSpeed(self.__currSpeed + amount)

    def slowDown(self, amount):
        self.setSpeed(self.__currSpeed - amount)

    def forward(self):
        self.__pi.write(self.__dir, 0) #may need to swap

    def reverse(self):
        self.__pi.write(self.__dir, 1) #may need to swap

    def hardStop(self):
        self.__pi.write(self.__break, 1)

class HallEffectSensor():
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
            print(f"output!")

        if (self.__currRevs == self.__revolutions + 1): #plus 1 means it went full circle
            rpmEndTime = time.time()
            rpmDelta = (rpmEndTime - self.__startTime)
            self.__startTime = time.time()
            self.__rpms = 1.0 / ((rpmDelta) / 60.0)
            self.__currRevs = 0

        return self.__rpms

class CurrentSensor():
    __channel = None
    __ZEROAMP = 513
    __HALFAMP = 7

    def __init__(self, channel):
        self.__channel = channel
        # Start SPI connection
        spi = spidev.SpiDev() # Created an object
        spi.open(0,0)

    # Read MCP3008 data
    def read(self):
      spi.max_speed_hz = 1350000
      adc = spi.xfer2([1,(8+self.__channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data

    def measureCurrent(self, samples):
        maxVal = 0
        for counter in range(samples):
            reading = self.read()
            if (reading > maxVal):
                maxVal = reading
        amps = ( (maxVal - self.__ZEROAMP) / self.HALFAMP ) / 2.0
        return amps
