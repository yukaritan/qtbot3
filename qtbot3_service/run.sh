#!/bin/sh

gunicorn --access-logfile - -w 10 -b 127.0.0.1:4000 service:app




