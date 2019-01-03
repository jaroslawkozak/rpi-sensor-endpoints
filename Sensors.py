import Adafruit_DHT
import datetime
import logging

logging.basicConfig(level=logging.DEBUG, filename="/var/log/sensorservice.log")
logger = logging.getLogger(__name__)


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
        self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio)
        self.check_buffer()
        return self

    # If measurement difference is too big, provides last measurement,
    # but if next reading is as big as previous, it sets the new one
    def check_buffer(self):
        if self.last_temperature is None:
            self.last_temperature = self.temperature
        elif self.__get_measure_diff(self.last_temperature, self.temperature) > self.buffer:
                DHT11.__log_buffer("temperature", self.last_temperature, self.temperature)
                tmp = self.last_temperature
                self.last_temperature = self.temperature
                self.temperature = tmp

        if self.last_humidity is None:
            self.last_humidity = self.humidity
        elif self.__get_measure_diff(self.last_humidity, self.humidity) > self.buffer:
                DHT11.__log_buffer("humidity", self.last_humidity, self.humidity)
                tmp = self.last_humidity
                self.last_humidity = self.humidity
                self.humidity = tmp

    @staticmethod
    def __get_measure_diff(prev, curr):
        return abs((float(curr)/float(prev))-1)

    @staticmethod
    def __log_buffer(name, prev, curr):
        logger.info("Buffering %s due to too high difference. "
                    "old (%s)  new (%s)", name, str(prev), str(curr))

    def data(self):
        return {
            'timestamp': str(datetime.datetime.utcnow()),
            'temperature': self.temperature,
            'humidity': self.humidity
        }
