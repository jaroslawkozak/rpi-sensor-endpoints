from flask import Response
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from Sensors import DHT11
from DataStorage import DataStorageUtil
import json

app = Flask('sensors-api')
dht11 = DHT11(17)


def store_sensor_data():
    dht11.read()
    DataStorageUtil.put("temperature", dht11.temperature)
    DataStorageUtil.put("humidity", dht11.humidity)


sched = BackgroundScheduler(daemon=True)
sched.add_job(store_sensor_data, 'interval', seconds=1)
sched.start()

@app.route("/metrics", methods=['GET'])
def get_sensors_data():
    dht11.read()
    json_message = json.dumps(dht11.data())
    return Response(json_message, status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True, threaded=True)



