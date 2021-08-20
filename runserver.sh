#! /bin/bash

gunicorn --chdir /Users/apasham/Downloads/test/fastapi-demo/src main:app -b :5000 -w 4 -k uvicorn.workers.UvicornWorker