from influxdb import InfluxDBClient
import datetime

INFLUX_DB_HOST = "192.168.0.200"
INFLUX_DB_PORT = 8086
INFLUX_DB_USER = "root"
INFLUX_DB_PASS = "root"
INFLUX_DB_NAME = "sensor-data"
SENSOR_NAME = "raspberry01"


class DataStorageUtil:

    def __init__(self):
        return

    @staticmethod
    def put(measurement_type, value):
        print("putting data: " + str(measurement_type) + " " + str(value) + " " + str(datetime.datetime.utcnow()))
        client = InfluxDBClient(INFLUX_DB_HOST, INFLUX_DB_PORT, INFLUX_DB_USER, INFLUX_DB_PASS, INFLUX_DB_NAME)
        client.create_database(INFLUX_DB_NAME)
        client.write_points(DataStorageUtil.format(measurement_type, value))

    @staticmethod
    def format(measurement_type, value):
        return [
            {
                "measurement": measurement_type,
                "tags": {
                    "sensor": SENSOR_NAME,
                },
                "time": datetime.datetime.utcnow(),
                "fields": {
                    "value": value
                }
            }
        ]