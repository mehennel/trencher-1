import pigpio #importing GPIO library

class Motor():
    __dir = None
    __speed = None
    __pi = None

    def __init__(self, pi, directionPin, speedPin):
        self.__pi = pi
        self.__dir - directionPin
        self.__speed = speedPin
        self.__pi.set_mode(self.__dir, pigpio.OUTPUT)
        self.__pi.set_mode(self.__speed, pigpio.OUTPUT)

    def setSpeed(self, speed):
        self.__pi.set_servo_pulsewidth(self.__speed, speed)

    def setDirection(self, direction):
        self.__pi.write(dir, 0)

    def ControlMotor(direction):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
        #start recording clock for tracking RPM data
        if direction == 'up' and pwm_value < 255:
            pwm_value += 5
        elif direction == 'down' and pwm_value > 0:
            pwm_value -= 5
        elif direction == 'space':
            print(f"Motor stopped")
            pwm_value = 0
        if pwm_value == 5:
             rpmStartTime = time.time()
