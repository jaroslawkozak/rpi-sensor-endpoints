from flask import Response
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from Sensors import DHT11
import json
import time

app = Flask('sensors-api')
dht11 = DHT11(17)

def write_sensor_to_file():
    dht11.read()
    with open('sensor-data.txt', 'a+') as f:
        f.write('timestamp: ' + str(int(round(time.time(), 0)))
                + 'temperature: '
                + str(dht11.temperature)
                + ', humidity: '
                + str(dht11.humidity) + '\n')


sched = BackgroundScheduler(daemon=True)
sched.add_job(write_sensor_to_file, 'interval', seconds=5)
sched.start()

@app.route("/metrics", methods=['GET'])
def get_sensors_data():
    dht11.read()
    json_message = json.dumps(dht11.data())
    return Response(json_message, status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True, threaded=True)



