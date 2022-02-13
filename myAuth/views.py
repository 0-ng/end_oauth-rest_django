import json
import time
import socket
import myAuth.encryp as encryp
# from rest.encryp import computePW, checkPW, createSalt
from myAuth.models import myUser
from django.http import JsonResponse
from django.contrib.auth.models import User


def jsonify(**kwargs):
    return JsonResponse(kwargs)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
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


# @app.route('/login', methods=["POST"])
def login(request):
    request.POST
    # print("1", request.form.__str__())
    print("2", request.values.__str__())
    print("3", request.get_data().__str__())
    print("4", request.get_json())
    username = request.values.get("username")
    password = request.values.get("password")
    print("username", username)
    print("password", password)
    if username == "" or password == "":
        code = "-1"
        data = {
            "msg": "Username or password is empty or invalid",
            "token": ""
        }
    else:
        result = myUser.objects.get(user__username=username)
        print(result)
        if result is None:
            code = "-1"
            data = {
                "msg": "wrong user name or password",
                "token": ""
            }
        else:
            localPW, salt = result.user.password, result.salt
            # localPW, salt = result[2], result[3]
            print("data", result)
            isConsistent = encryp.checkPW(encryp.computePW(password, salt), localPW)
            if isConsistent:
                code = "0"
                data = {
                    "msg": "Login verification succeeded",
                    "token": f"oauth.{username}"
                }
                # token = jwt.encode({"username": username}, my_secretKey, "HS256")
                # session["logintime"] = getlocaltime()
                # session["isLogin"] = True
                # session["username"] = username
                print(f"{username}用户登录成功")
            else:
                code = "-1"
                data = {
                    "msg": "wrong user name or password",
                    "token": ""
                }
                print("%s用户登录输入密码错误,登录失败" % username)

    resp = jsonify(code=code, data=data)
    return resp


# @app.route('/')
def hello(request):
    resp = jsonify(code=200, msg=get_host_ip())
    return resp


# @app.route('/portalLogin', methods=["POST"])
def portalLogin(request):
    print("1", request.form.__str__())
    print("2", request.values.__str__())
    print("3", request.get_data().__str__())
    print("4", request.get_json())
    code = request.values.get("code")
    username, token = myUser.getPortalAuthorizationByCode(code)
    print(username, token)
    code = "0"
    msg = ""
    if username is None:
        code = "-1"
        msg = "username is null"
        token = None
    else:
        if username == "admin":
            if encryp.getPortalRestByToken(token) != "B" and encryp.getPortalWebByToken(token) != "B":
                code = "-1"
                msg = "token not match"
                token = None
        else:
            if encryp.getPortalRestByToken(token) != "A" and encryp.getPortalWebByToken(token) != "A":
                code = "-1"
                msg = "token not match"
                token = None
    resp = jsonify(code=code, data={"token": token, "msg": msg})
    return resp

# @app.route('/getEnv', methods=["POST"])
def getEnv(request):
    print("1", request.form.__str__())
    print("2", request.values.__str__())
    print("3", request.get_data().__str__())
    print("4", request.get_json())
    token = request.values.get("oauth_token")
    print("token", token)
    reqEnv, username = token.split(".")
    if reqEnv != "oauth":
        resp = jsonify(code=-1, data={"msg": "env error"})
        return resp
    respEnv = {
        "portal_rest": 'B',
        "portal_web": 'B',
        # "redirectUrl": "http://portal-web-a/"
        "redirectUrl": "http://127.0.0.1:8002/"
    }
    if username != "admin":
        respEnv = {
            "portal_rest": 'A',
            "portal_web": 'A',
            # "redirectUrl": "http://portal-web-a/"
            "redirectUrl": "http://127.0.0.1:8001/"
        }
        # respEnv["portal_rest"] = 'A',
        # respEnv["portal_web"] = 'A',
        # # respEnv["redirectUrl"] = "http://portal-web-b/"
        # respEnv["redirectUrl"] = "http://127.0.0.1:8001/"
    code = myUser.generateAUTHORIZATION(username, respEnv["portal_rest"], respEnv["portal_web"])
    resp = jsonify(code=0, data={"env": respEnv, "code": code})
    return resp


# @app.route('/createUser', methods=["POST"])
def createUser(request):
    username = request.form.get("username", type=str, default="")
    password = request.form.get("password", type=str, default="")
    print(username)
    if username == "" or password == "":
        code = "-2"
        msg = "username or password null"
    else:
        user = myUser.objects.get(user__username=username)
        if user is not None:
            code = "-1"
            msg = "user existed"
        else:
            user = User(username=username, password=password)
            my_user = myUser(user=user)
            my_user.save()
            code = "0"
            msg = "create succeeded"
    resp = jsonify(code=code, msg=msg)
    return resp


# @app.route('/getAllUserInfos', methods=["GET"])
def getAllUserInfos(request):
    code = "0"
    msg = json.dumps(myUser.objects.all())
    resp = jsonify(code=code, msg=msg)
    return resp


def equal(b: bytes):
    """用来补齐被JWT去掉的等号"""
    rest = len(b) % 4
    return b + '='*rest




if __name__ == '__main__':
    pass
    # print(f(a=1, b=2, c="asd"))
#     db_init()
#     # data = jsonify(a='1', b='2')
#     # print(data)
#     # resp = jsonify(code=200, data=data)
#     # print(resp)
#     app.run(debug=True)
#
#     # key = "secret"
#     # token = jwt.encode({"test": "100"}, key, "HS256")
#     # header, payload, signature = token.split(".")
#     #
#     # print("header=",base64.urlsafe_b64decode(equal(header)))
#     # print("payout=", base64.urlsafe_b64decode(equal(payload)))
#     # print("signature", base64.urlsafe_b64decode(equal(signature)))

