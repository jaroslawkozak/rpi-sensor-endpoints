#!/usr/bin/python
import os
os.system('sudo docker stop sensor-service')
os.system('sudo docker rm sensor-service')
os.system('sudo docker image rm sensor-service')
os.system('sudo docker build --no-cache . -f Dockerfile-rpi -t sensor-service:latest')
os.system('sudo docker run --privileged --name sensor-service -d -p 5555:5555 sensor-service')


