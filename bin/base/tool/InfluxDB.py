from influxdb import InfluxDBClient


class InfluxDB(object):
    def __init__(self, ds=None, host='127.0.0.1', port=8086, user='root', pwd='root', db='example'):
        if ds is not None:
            host = ds.get('host', '127.0.0.1')
            port = ds.get('port', 8086)
            user = ds.get('user', 'root')
            pwd = ds.get('pwd', 'root')
            db = ds.get('db', 'example')
        self.client = InfluxDBClient(host=host, port=port, username=user, password=pwd, database=db)
        self.client.create_database(db)  # 默认去建立数据库

    # 创建数据库
    def create_database(self, db_name):
        self.client.create_database(db_name)

    # 删除数据库
    def drop_database(self, db_name):
        self.client.drop_database(dbname=db_name)

    # 写入数据
    def write_points(self, point):
        self.client.write_points(point)

    def query(self, sql):
        return self.client.query(sql)
    def get_
    # from influxdb import InfluxDBClient
    # import datetime
    #
    # current_time = datetime.datetime.utcnow().isoformat("T")
    # json_body = [
    #     {
    #         "measurement": "cpu_load_short",  # 测量指标名称
    #         "tags": {
    #             "host": "192.168.6.22",
    #             "region": "us-west"
    #         },
    #         "time": current_time,
    #         "fields": {
    #             "value": 0.66
    #         }
    #     }
    # ]
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00'))
    # print(datetime.datetime.utcnow())
    # client = InfluxDBClient('192.168.7.219', 8086, 'root', 'root', 'example')
    #
    # client.create_database('example')
    #
    # client.write_points(json_body)
    #
    # # print('\n删除表\n')
    # # client.drop_measurement('table1')
    # # client.query("drop measurement table1")
    # # print('删除数据库\n')
    # # client.drop_database('mytestdb')
    # # class influxdb.InfluxDBClient(host=u'localhost', port=8086, username=u'root', password=u'root', database=None, ssl=False, verify_ssl=False, timeout=None, retries=3, use_udp=False, udp_port=4444, proxies=None)
    # result = client.query('select value from cpu_load_short limit 3 offset 2;')
    #
    # print("Result: {0}".format(result))


def getInstance(ds=None, host='127.0.0.1', port=8086, user='root', pwd='root', db='example'):
    return InfluxDB(ds=ds, host=host, port=port, user=user, pwd=pwd, db=db)
