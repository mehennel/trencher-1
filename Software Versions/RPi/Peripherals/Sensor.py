from abc import ABC, abstractmethod

class Sensor(ABC):
    @abstractmethod
    def read(self):
        pass
