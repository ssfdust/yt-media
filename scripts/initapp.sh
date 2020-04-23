#!/bin/sh
flask db upgrade
gunicorn -k egg:meinheld#gunicorn_worker -c gunicorn.py smorest_sfs.app:app
