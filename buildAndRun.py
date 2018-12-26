#!/usr/bin/python
import os
os.system('sudo docker build . -f Dockerfile-rpi')
os.system('sudo docker run --privileged --name sensor-service -d -p 5555:5555 sensor-service')



