# !/usr/bin/env python
# !-*- coding:utf-8 -*-

import pika
from bin import init
from bin.base.log import Logger
from bin.base.data import Data

L = Logger.getInstance('sys.log')


class RabbitMQ(object):
    def __init__(self, MQCONF=None, ds=None, path='/', timeout=10):
        self.connection = None
        if MQCONF is not None:
            host = MQCONF.get('toolHost', '127.0.0.1')
            port = MQCONF.get('toolPort', 5672)
            user = MQCONF.get('toolUser', None)
            password = MQCONF.get('toolPassword', None)
            path = MQCONF.get('path', path)
            credentials = pika.PlainCredentials(user, password)
            par = pika.ConnectionParameters(host=host, port=port, virtual_host=path, credentials=credentials, socket_timeout=timeout)
            self.connection = pika.BlockingConnection(par)  # 创建连接
        elif ds is not None:
            info = init.CONF_INFO.get(ds)
            host = info.get('toolHost', '127.0.0.1')
            port = info.get('toolPort', 5672)
            user = info.get('toolUser', None)
            password = info.get('toolPassword', None)
            path = info.get('path', path)
            credentials = pika.PlainCredentials(user, password)
            par = pika.ConnectionParameters(host=host, port=port, virtual_host=path, credentials=credentials, socket_timeout=timeout)
            self.connection = pika.BlockingConnection(par)  # 创建连接
        else:
            pass

    # msg 仅接受json格式数据
    # msg 为字符串格式时为消息、记录存储
    def sendMsg(self, queue=None, msg=None):
        if self.connection is None:
            L.error('QM init info error ,sendMsg has not connection')
            return None
        if queue is None:
            queue = init.ROOT_MQ_DEFAULT_QUEUE
        queue = init.CONTEXT + queue
        msg = Data.json_to_str(msg)
        # 声明一个管道，在管道里发消息
        channel = self.connection.channel()
        # 在管道里声明queue
        channel.queue_declare(queue=queue, durable=True)  # durable的作用只是把队列持久化。离消息持久话还差一步：
        channel.basic_publish(exchange='', routing_key=queue, body=msg, properties=pika.BasicProperties(delivery_mode=2))  # delivery_mode=2 消息持久化
        self.connection.close()

    def receiveMsg(self, queue=None, callback=None):
        if callback is None:
            L.error('MQ receiveMsg not set callback')
            return None
        if self.connection is None:
            L.error('QM init info error ,receiveMsg has not connection')
            return None
        if queue is None:
            queue = init.ROOT_MQ_DEFAULT_QUEUE
        queue = init.CONTEXT + queue
        channel = self.connection.channel()
        # 声明消息队列，消息将在这个队列中进行传递。如果队列不存在，则创建
        channel.queue_declare(queue=queue, durable=True)
        # 告诉rabbitmq使用callback来接收信息
        # channel.basic_consume(callback, queue=queue, no_ack=False) # 0.1.11版本
        channel.basic_consume(on_message_callback=callback, queue=queue, auto_ack=False)  # 1.1.0 版本

        # 公平分发，使每个consumer在同一时间最多处理一个message，收到ack前，不会分配新的message
        # channel.basic_qos(prefetch_size=0, prefetch_count=1, all_channels=False) # 0.1.11版本
        channel.basic_qos(prefetch_size=0, prefetch_count=1, global_qos=False)  # 1.1.0 版本

        channel.start_consuming()  # 无阻塞是消费

    # 获取队列中消息数量
    def getQueueMsgCount(self, queue=None):
        if queue is None:
            queue = init.ROOT_MQ_DEFAULT_QUEUE
        channel = self.connection.channel()
        ch = channel.queue_declare(queue=queue, durable=True, passive="passive")
        count = ch.method.message_count
        self.connection.close()
        return count

    # 发布消息
    def publishMsg(self, exchange='default', routing_key='', exchange_type='default', msg={}):
        msg = Data.json_to_str(msg)
        channel = self.connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)
        self.connection.close()

    # 订阅消息
    def readMsg(self, exchange='default', exchange_type='default', queue_name='readMsg', callback=None):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        channel.queue_bind(exchange=exchange, queue=queue_name)
        channel.basic_consume(callback, queue=queue_name, no_ack=True, )
        channel.start_consuming()
        # exclusive=True会在使用此queue的消息订阅端断开后,自动将queue删除
        # 不指定queue名字,rabbitmq会随机分配一个名字
        # result = channel.queue_declare(exclusive=True)
        # queue_name = result.method.queue
        # print('当前queue名称：', queue_name)

    # callback 示例
    def callback(self, ch, method, properties, body):
        pass

    # # 建立一个实例
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters('localhost', 5672)  # 默认端口5672，可不写
    # )
    # # 声明一个管道，在管道里发消息
    # channel = connection.channel()
    # # 在管道里声明queue
    # channel.queue_declare(queue='hello')
    # # RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
    # channel.basic_publish(exchange='',
    #                       routing_key='hello',  # queue名字
    #                       body='Hello World!')  # 消息内容
    # print(" [x] Sent 'Hello World!'")
    # connection.close()  # 队列关闭
    # #######################################################################
    # # 建立实例
    # connection = pika.BlockingConnection(pika.ConnectionParameters(
    #     'localhost'))
    # # 声明管道
    # channel = connection.channel()
    #
    # # 为什么又声明了一个‘hello’队列？
    # # 如果确定已经声明了，可以不声明。但是你不知道那个机器先运行，所以要声明两次。
    # channel.queue_declare(queue='hello')
    #
    # def callback(ch, method, properties, body):  # 四个参数为标准格式
    #     print(ch, method, properties)  # 打印看一下是什么
    #     # 管道内存对象  内容相关信息  后面讲
    #     print(" [x] Received %r" % body)
    #     time.sleep(15)
    #     ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成
    #
    # channel.basic_consume(  # 消费消息
    #     callback,  # 如果收到消息，就调用callback函数来处理消息
    #     queue='hello',  # 你要从那个队列里收消息
    #     # no_ack=True  # 写的话，如果接收消息，机器宕机消息就丢了
    #     # 一般不写。宕机则生产者检测到发给其他消费者
    # )
    #
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()  # 开始消费消息


def getInstance(MQCONF=None, ds=None, path='/', timeout=10):
    return RabbitMQ(MQCONF=MQCONF, ds=ds, path=path, timeout=timeout)
