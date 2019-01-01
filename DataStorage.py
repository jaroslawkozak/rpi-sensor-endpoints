from influxdb import InfluxDBClient
import config
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataStorageUtil:

    def __init__(self):
        return

    @staticmethod
    def put(measurement_type, value):
        logging.debug("Sending data for storage. %s: %s", measurement_type, value)
        client = InfluxDBClient(config.INFLUX_DB_CONFIG['host'],
                                config.INFLUX_DB_CONFIG['port'],
                                config.INFLUX_DB_CONFIG['username'],
                                config.INFLUX_DB_CONFIG['password'],
                                config.INFLUX_DB_CONFIG['db_name'])
        client.create_database(config.INFLUX_DB_CONFIG['db_name'])
        client.write_points(DataStorageUtil.format(measurement_type, value))

    @staticmethod
    def format(measurement_type, value):
        return [
            {
                "measurement": measurement_type,
                "tags": {
                    "sensor": config.SENSOR_CONFIG['name'],
                },
                "time": datetime.datetime.utcnow(),
                "fields": {
                    "value": value
                }
            }
        ]