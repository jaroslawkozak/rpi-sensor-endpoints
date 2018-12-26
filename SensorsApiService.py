from flask import request, Response
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from Sensors import DHT11
import Adafruit_DHT
import json

app = Flask('sensors-api')


def write_sensor_to_file():
    dht = read_sensor()
    with open('sensor-data.txt', 'ab+') as f:
        print('added: Temperature: ' + dht.temperature + ', Humidity: ' + dht.humidity)
        f.write('Temperature: ' + dht.temperature + ', Humidity: ' + dht.humidity + '\n')


sched = BackgroundScheduler(daemon=True)
sched.add_job(write_sensor_to_file, 'interval', minutes=1)
sched.start()


def read_sensor():
    # Set sensor type : Options are DHT11,DHT22 or AM2302
    sensor = Adafruit_DHT.DHT11

    # Set GPIO sensor is connected to
    gpio = 17

    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

    dht = DHT11(temperature, humidity)
    return dht


@app.route("/metrics", methods=['GET'])
def get_sensors_data():
    dht = read_sensor()

    json_message = json.dumps(dht.__dict__)
    return Response(json_message, status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True, threaded=True)



