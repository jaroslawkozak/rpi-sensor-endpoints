import Adafruit_DHT
import datetime

class DHT11:

    def __init__(self, gpio):
        # Set sensor type : Options are DHT11,DHT22 or AM2302
        self.sensor = Adafruit_DHT.DHT11
        self.gpio = gpio
        self.humidity = None
        self.temperature = None
        self.last_humidity = None
        self.last_temperature = None
        self.buffer = 0.3

    def read(self):
        # Use read_retry method. This will retry up to 15 times to
        # get a sensor reading (waiting 2 seconds between each retry).
        print("reading data: " + str(datetime.datetime.utcnow()))
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio)
        self.check_buffer()
        return self

    # If measurement difference is too big, provides last measurement,
    # but if next reading is as big as previous, it sets the new one
    def check_buffer(self):
        if self.last_temperature is None:
            self.last_temperature = self.temperature
        elif self.temperature > (self.last_temperature * (1 + self.buffer)):
            tmp = self.last_temperature
            self.last_temperature = self.temperature
            self.temperature = tmp
        elif self.temperature < (self.last_temperature * (1 - self.buffer)):
            tmp = self.last_temperature
            self.last_temperature = self.temperature
            self.temperature = tmp

        if self.last_humidity is None:
            self.last_humidity = self.humidity
        elif self.humidity > (self.last_humidity * (1 + self.buffer)):
            tmp = self.last_humidity
            self.last_humidity = self.humidity
            self.humidity = tmp
        elif self.humidity < (self.last_humidity * (1 - self.buffer)):
            tmp = self.last_humidity
            self.last_humidity = self.humidity
            self.humidity = tmp

    def data(self):
        return {
            'timestamp': str(datetime.datetime.utcnow()),
            'temperature': self.temperature,
            'humidity': self.humidity
        }