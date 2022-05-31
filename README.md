![logo](img/canaspad_logo.png)
# Canaspad API
![GitHub](https://img.shields.io/github/license/spadr/IoT_Frame_ops)

Canaspad is a data analytics infrastructure for IoT! 
You can install Canaspad API and Docker Compose in your own Web server and and can send & receive sensing data and control microcontroller.
You can make your home a smart home, install smart agriculture in your greenhouse, check analog gauges with your smartphone, etc.


## Installation
### Install on RaspberryPi
see at https://github.com/spadr/IoT_Frame_RaspberryPi
### Install on x86-64 machine
1. Install Docker Engine on your server
2. Install Docker Compose V1 on your server
3. Git clone this repository
<br>$ git clone https://github.com/spadr/IoT_Frame_ops.git
4. Move to cloned repository
<br>$ cd IoT_Frame_ops
5. Rename "env.example" to ".env"
<br>$ mv .env.example .env
6. Build image and launch each container
<br>$ sudo docker-compose -f docker-compose.yml up -d --build
7. Check the health of dokcer containers
<br>$ sudo docker-compose -f docker-compose.yml ps -a
8. Execution of dead/alive monitoring scripts
<br>$ sudo docker-compose -f docker-compose.yml exec app python manage.py alive_monitoring