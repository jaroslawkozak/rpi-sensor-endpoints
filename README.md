# rpi-sensor-endpoints

This repo is designed to run on Raspberry Pi, as Docker container.

To use it, pull repo and run command:
```
python buildAndRun.py
```
which will, clean old container if present, prepare and run new one.
(at this stage of project, some ip's are hardcoded, so watch out)

For sensor endpoint to run correctly, a Pi should also have an instance of influxDB running:
```
sudo docker run -d --restart=unless-stopped -p 8086:8086 --name influxdb -v influxdb:/var/lib/influxdb arm32v7/influxdb
```

Additionaly, Pi can have graphana instance for sensor data visualization:
```
sudo docker run -d --restart=unless-stopped -p 3000:3000 --name grafana fg2it/grafana-armhf:v5.1.4
```

Unfortunately, at this stage, all configuration is hardcoded, and it works on local network only
