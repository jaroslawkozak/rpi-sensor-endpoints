import Adafruit_DHT
import datetime

class DHT11:
    def __init__(self, gpio):
        # Set sensor type : Options are DHT11,DHT22 or AM2302
        self.sensor = Adafruit_DHT.DHT11
        self.gpio = gpio
        self.humidity = None
        self.temperature = None

    def read(self):
        # Use read_retry method. This will retry up to 15 times to
        # get a sensor reading (waiting 2 seconds between each retry).
        print "reading data: " + datetime.datetime.utcnow()
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio)
        return self

    def data(self):
        return {
            'timestamp': datetime.datetime.utcnow(),
            'temperature': self.temperature,
            'humidity': self.humidity
        }