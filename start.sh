#!/bin/bash
gunicorn "sa_ba_:app" --bind 0.0.0.0:$PORT
