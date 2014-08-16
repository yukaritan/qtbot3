#!/bin/sh

screen -S qtbot3service gunicorn --access-logfile - -w 10 -b 127.0.0.1:4000 service:app
