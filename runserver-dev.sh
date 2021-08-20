#! /bin/bash

# python src/main.py

uvicorn --app-dir /Users/apasham/Downloads/test/fastapi-demo/src main:app --host 127.0.0.1 --port=5000 --env-file=.env --reload