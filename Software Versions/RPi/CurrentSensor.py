import spidev # To communicate with SPI devices

class CurrentSensor(Sensor):
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
