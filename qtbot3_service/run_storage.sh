#!/bin/sh

screen -S qtbot3storage gunicorn --access-logfile - -w 1 -b 127.0.0.1:4001 storage:app
