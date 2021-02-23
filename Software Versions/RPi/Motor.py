import pigpio #importing GPIO library

class Motor():
    __dir = None
    __speed = None
    __pi = None
    __break = None
    __currSpeed = None

    def __init__(self, pi, sv, fr, brk):
        self.__pi = pi
        self.__speed = sv
        self.__dir - fr
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
