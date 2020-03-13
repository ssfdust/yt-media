# Copyright 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    app.extensions.rpcstore
    ~~~~~~~~~~~~~~~~~~~~~~~~

    rabbitMQ存储模块
"""

from flask import current_app
from kombu import Connection
from kombu import Exchange, Queue
from kombu.pools import producers, connections
from amqp.exceptions import NotFound


class AMQPStore:
    """
    存储器

    :param value: 值
    :param exchange: 交换机名
    :param expires: 过期时长
    :param limit: 最大限制
    :parma routing_key: 路由名
    :param auto_delete: 是否自动删除
    """

    def __init__(self, key, value=None, exchange=None, **kwargs):
        self.key = key
        self.value = value
        self.values = []
        self.msgs = []
        self.exchange = Exchange(exchange)
        self.limit = kwargs.get("limit", 999)
        self.max_length = kwargs.get("max_length")
        self.routing_key = kwargs.get("routing_key")
        self.queue = Queue(
            self.key,
            self.exchange,
            durable=True,
            max_length=kwargs.get("max_length"),
            routing_key=self.routing_key,
            auto_delete=kwargs.get("auto_delete", False),
            expires=kwargs.get("expires"),
        )

    def save(self, expiration=None):
        """ 保存

        :param expiration 过期时间
        """
        conn = Connection(current_app.config["CELERY_BROKER_URL"], heartbeat=0)

        with producers[conn].acquire(block=True) as producer:
            producer.publish(
                self.value,
                exchange=self.exchange,
                routing_key=self.routing_key,
                correlation_id=self.routing_key,
                serializer="json",
                retry=True,
                declare=[self.queue],
                delivery_mode=2,
                expiration=expiration,
            )

        return self.value

    def reload(self, no_ack=False, requeue=False):
        """
        重载数值
        """
        self.value = None
        self.values = []
        self._collect_msgs(no_ack)
        self._handle_msgs(no_ack, requeue)

        return self.value

    @staticmethod
    def calculate_requeue_able(no_ack, requeue):
        if no_ack is False and requeue is False:
            return False
        return True

    def _handle_msgs(self, no_ack, requeue):
        if no_ack:
            return
        if self.calculate_requeue_able(no_ack, requeue):
            self._requeue_msgs()
        else:
            self._ack_msgs()

    def _requeue_msgs(self):
        for msg in self.msgs:
            msg.requeue()

    def _ack_msgs(self):
        for msg in self.msgs:
            msg.ack()

    def _collect_msgs(self, no_ack):
        self.msgs = []
        for i in self.extract_from_queue(no_ack):
            self.value = i.payload
            self.values.append(self.value)
            self.msgs.append(i)

    def extract_from_queue(self, no_ack=False):
        """
        从队列加载并返回列表
        """
        conn = Connection(current_app.config["CELERY_BROKER_URL"], heartbeat=0)
        pool = connections[conn]

        with pool.acquire_channel(block=True) as (_, channel):
            binding = self.queue(channel)

            for _ in range(self.limit):
                try:
                    msg = binding.get(accept=["json"], no_ack=no_ack)
                    if not msg:
                        break
                    yield msg
                except NotFound:
                    break
