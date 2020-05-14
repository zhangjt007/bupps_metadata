import socket
import time


class IdWorker(object):
    # 获取主机名
    HOSTNAME = socket.gethostname()
    # 获取IP
    IP = socket.gethostbyname(HOSTNAME)
    # 序列号(12位  0-4095)
    SERIAL_NUMBER = 0
    # 时间戳（41位）
    TIMESTAMP = int(time.time() * 1000)
    # 机器id(10位  0-1024)  这里取机器ip最后8位
    MACHINE_ID = int(IP.split('.')[3])

    @classmethod
    def generate(cls):
        now = int(time.time() * 1e3)
        if now == cls.TIMESTAMP:
            cls.SERIAL_NUMBER += 1
        else:
            cls.TIMESTAMP = now
            cls.SERIAL_NUMBER = 0
        return (cls.TIMESTAMP << 22) + (cls.MACHINE_ID << 12) + cls.SERIAL_NUMBER


if __name__ == '__main__':
    import random

    for i in range(100):
        time.sleep(random.random())
        _id = IdWorker.generate()
        print(_id)
