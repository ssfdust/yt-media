#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.app import app
from smorest_sfs.extensions import redis_store


def sub():
    with app.app_context():
        pubsub = redis_store.pubsub()
        pubsub.subscribe(["channel"])
        for item in pubsub.listen():
            print("%s" % (item["data"]))


if __name__ == "__main__":
    sub()
