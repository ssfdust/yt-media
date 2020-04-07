#!/bin/sh
if [ ! -e "/var/www/application/inited_app" ];then
    mkdir -p /var/www/application
    touch /var/www/application/inited_app
    inv app.init.initdb
    inv app.init.init-development-data
fi
inv app.run -b 0.0.0.0:5000
