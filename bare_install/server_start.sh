#!/bin/bash

gunicorn app:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --pid gunicorn.pid -D