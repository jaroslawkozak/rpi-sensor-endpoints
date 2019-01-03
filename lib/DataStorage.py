from influxdb import InfluxDBClient
import config
import datetime
import time
import logging
import os
import socket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MetricStorage:
    client = InfluxDBClient(config.INFLUX_DB_CONFIG['host'],
                            config.INFLUX_DB_CONFIG['port'],
                            config.INFLUX_DB_CONFIG['username'],
                            config.INFLUX_DB_CONFIG['password'],
                            config.INFLUX_DB_CONFIG['db_name'])
    client.create_database(config.INFLUX_DB_CONFIG['db_name'])

    def __init__(self):
        return

    @staticmethod
    def put(measurement_type, value):
        msg = "Sending data for storage. %s: %s", measurement_type, value
        logging.info(msg)
        LogStorage.log('info', msg)
        MetricStorage.client.write_points(MetricStorage.format(measurement_type, value))

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


class LogStorage:
    client = InfluxDBClient(config.INFLUX_DB_CONFIG['host'],
                            config.INFLUX_DB_CONFIG['port'],
                            config.INFLUX_DB_CONFIG['username'],
                            config.INFLUX_DB_CONFIG['password'],
                            config.INFLUX_DB_CONFIG['log_db_name'])
    client.create_database(config.INFLUX_DB_CONFIG['log_db_name'])

    def __init__(self):
        return

    @staticmethod
    def log(severity, msg):
        LogStorage.client.write_points(LogStorage.format(severity, msg))

    @staticmethod
    def format(severity, msg):
        return [
            {
                "measurement": "syslog",
                "tags": {
                    "appname": config.APP_CONFIG['app_name'],
                    "facility": "console",
                    "host": socket.gethostname(),
                    "hostname": socket.gethostname(),
                    "severity": severity
                },
                "fields": {
                    "facility_code": 1,
                    "message": msg,
                    "procid": str(os.getpid()),
                    "severity_code": 1,
                    "timestamp": int(time.time()),
                    "version": 1
                }
            }
        ]
