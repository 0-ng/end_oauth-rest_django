import json
import myAuth.encryp as encryp
from myAuth.models import myUser
from django.contrib.auth.models import User
from django.contrib import auth
from myAuth.common import *


# @app.route('/login', methods=["POST"])
@requires_POST
def login(request):
    print("login", request.POST)
    username = request.POST["username"]
    password = request.POST["password"]
    print("username", username)
    print("password", password)
    if username == "" or password == "":
        # 用户名/密码格式错误
        code = "-1"
        data = {
            "msg": "Username or password is empty or invalid",
            "token": ""
        }
        resp = jsonify(code=code, data=data)
        return resp

    try:
        # 存在用户判断密码是否正确
        myUser.objects.get(user__username=username)
        print("?")
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            code = "0"
            data = {
                "msg": "Login verification succeeded",
                "token": f"oauth.{username}"
            }
            print(f"{username}用户登录成功")
        else:
            code = "-1"
            data = {
                "msg": "wrong user name or password",
                "token": ""
            }
            print("%s用户登录输入密码错误,登录失败" % username)
    except:
        # 不存在用户,自动创建
        resp = createUser(username, password)
        if resp["code"] != "0":
            print(resp["msg"])
        code = "0"
        data = {
            "msg": "creat user succeed",
            "token": f"oauth.{username}"
        }

    resp = jsonify(code=code, data=data)
    return resp



# check
def createUser(username, password):
    print("create user", username, password)
    if username == "" or password == "":
        code = "-2"
        msg = "username or password null"
        resp = {"code": code, "msg": msg}
        return resp

    user = myUser.objects.filter(user__username=username)
    if user.count() != 0:
        code = "-1"
        msg = "user existed"
        resp = {"code": code, "msg":msg}
        return resp
    user = User.objects.create_user(username=username, password=password)
    my_user = myUser(user=user)
    my_user.save()
    code = "0"
    msg = "create succeeded"
    resp = {"code": code, "msg": msg}
    return resp


# @app.route('/')
#check
def hello(request):
    resp = jsonify(code="0", msg=get_host_ip())
    return resp


# @app.route('/getEnv', methods=["POST"])
@requires_POST
def getEnv(request):
    token = request.POST["oauth_token"]
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
    code = myUser.generateAUTHORIZATION(username, respEnv["portal_rest"], respEnv["portal_web"])
    resp = jsonify(code=0, data={"env": respEnv, "code": code})
    return resp


# @app.route('/portalLogin', methods=["POST"])
@requires_POST
def portalLogin(request):
    code = request.POST["code"]
    username, token = myUser.getPortalAuthorizationByCode(code)
    print(username, token)
    code = "0"
    msg = ""
    if username is None:
        code = "-1"
        msg = "username is null"
        token = None
        resp = jsonify(code=code, data={"token": token, "msg": msg})
        return resp

    # if username == "admin":
    #     if encryp.getPortalRestByToken(token) != "B" and encryp.getPortalWebByToken(token) != "B":
    #         code = "-1"
    #         msg = "token not match"
    #         token = None
    # else:
    #     if encryp.getPortalRestByToken(token) != "A" and encryp.getPortalWebByToken(token) != "A":
    #         code = "-1"
    #         msg = "token not match"
    #         token = None
    resp = jsonify(code=code, data={"token": token, "msg": msg})
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
    return b + '=' * rest


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
