# rpi-sensor-endpoints

This repo is designed to run on Raspberry Pi, as Docker container.

For it to run correctly, a Pi should also have an instance of influxDB running:
```
sudo docker run -d --restart=unless-stopped -p 8086:8086 --name influxdb -v influxdb:/var/lib/influxdb arm32v7/influxdb
```

Additionaly, Pi can have graphana instance for sensor data visualization:
```
sudo docker run -d --restart=unless-stopped -p 3000:3000 --name grafana fg2it/grafana-armhf:v5.1.4
```

Unfortunately, at this stage, all configuration is hardcoded, and it works on local network only
