from smorest_sfs.app import app
from smorest_sfs.extensions import redis_store
import time


def pub():
    with app.app_context():
        for n in range(10):
            redis_store.publish("channel", "blah %d" % n)
            time.sleep(1)


if __name__ == "__main__":
    pub()
