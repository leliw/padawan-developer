#!/bin/sh
set -e
service ssh start
exec gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app