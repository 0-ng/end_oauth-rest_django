from django.http import JsonResponse
import time
import socket
from functools import wraps


def requires_POST(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if args[0].method != "POST":
            code = "-1"
            data = {
                "msg": "wrong request method",
                "token": ""
            }
            resp = jsonify(code=code, data=data)
            return resp
        return f(*args, **kwargs)

    return decorated


def jsonify(**kwargs):
    return JsonResponse(kwargs)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def getlocaltime():
    """格式化当前时间

    :return: 字符串格式的当前调用时间
    """
    datetime = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time())).encode("utf-8")
    return datetime

