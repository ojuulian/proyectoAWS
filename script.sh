#!/bin/bash
echo Starting my app.
cd  /home/ubuntu/final/proyectoAWS
. venv/bin/activate
sudo gunicorn --workers=5 -b 0.0.0.0:443 --certfile=micertificado.pem --keyfile=llaveprivada.pem wsgi:application