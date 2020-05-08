#!/bin/sh
flask db upgrade
if [ "$APP" = "web" ];then
    gunicorn -k egg:meinheld#gunicorn_worker -c gunicorn.py smorest_sfs.app:app
elif [ "$APP" = "celery" ];then
    celery --app=smorest_sfs.app:celery_app worker -l INFO -E
elif [ "$APP" = "beat" ];then
    celery beat --app=smorest_sfs.app:celery_app -S redbeat.RedBeatScheduler
fi
