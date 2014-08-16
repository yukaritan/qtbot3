#!/bin/sh

screen -S qtbot3client gunicorn --access-logfile - -w 1 -b 127.0.0.1:4002 main:app