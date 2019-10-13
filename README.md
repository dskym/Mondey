# YAPP

sudo apt-get install python3.6-dev libmysqlclient-dev

Install python3
Install python3-pip
Install nginx
Install python3-venv

(venv) install Django
(venv) install uwsgi

pip install mysqlclient 

 pip install --upgrade setuptools


.key and .csr
# openssl req -new -newkey rsa:2048 -nodes -keyout <파일명>.key -out <파일명>l.csr

Self sign
openssl x509 -req -days 365 -in <파일명>.csr -signkey <파일명>.key -out <파일명>.crt

