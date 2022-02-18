from myAuth.encryp import createSalt
from django.db import models
from django.contrib.auth.models import User
import jwt
from myAuth.config import my_secretKey


class myUser(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    salt = models.TextField(blank=True)
    authorization = models.TextField(blank=True)  # portal-web鉴权码 放header
    code = models.TextField(blank=True)  # portal-web授权码 放url参数

    # def __init__(self, username, password):
    #     self.username = username
    #     salt = createSalt()
    #     self.password = computePW(password, salt)
    #     self.salt = salt
    #     self.authorization = ""
    #     self.token = ""
    #
    # def save(self):
    #     if User.queryByName(self.username) is None:
    #         conn = get_conn()
    #         cursor = conn.cursor()
    #         sql = "INSERT INTO USER VALUES (?,?,?,?,?,?)"
    #         cursor.execute(sql, (User.rowCount() + 1, self.username, self.password, self.salt, "", ""))  # 执行sql语句
    #         conn.commit()  # 提交数据库改动
    #         cursor.close()  # 关闭游标
    #         conn.close()  # 关闭数据库连接
    #
    @staticmethod
    def generateAUTHORIZATION(username, rest, web):
        code = createSalt()
        data = {'username': username,
                'portal_rest': rest,
                'portal_web': web
                }
        authorization = jwt.encode(data, my_secretKey, algorithm='HS256')

        user = myUser.objects.get(user__username=username)
        user.authorization = authorization
        user.code = code
        user.save()
        print(username, "generate AUTHORIZATION succeed", code)
        return code

    @staticmethod
    def getPortalAuthorizationByCode(code):
        authorization = None
        username = None
        try:
            user = myUser.objects.get(code=code)
            authorization = user.authorization
            username = user.user.username
        except:
            pass
        print("get Portal Token By Code", code)
        return username, authorization
    #
    # @staticmethod
    # def all():
    #     sql = "SELECT * FROM USER"
    #     conn = get_conn()
    #     cursor = conn.cursor()
    #     users = cursor.execute(sql).fetchall()
    #     cursor.close()
    #     conn.close()
    #     return users
    #
    # @staticmethod
    # def queryByName(username):
    #     sql = "SELECT * FROM USER WHERE username=?"
    #     conn = get_conn()
    #     cursor = conn.cursor()
    #     users = cursor.execute(sql, (username,)).fetchall()
    #     cursor.close()
    #     conn.close()
    #     if len(users) == 0:
    #         return None
    #     return users[0]
    #
    # @staticmethod
    # def rowCount():
    #     return len(User.all())
    #
    # def __str__(self):
    #     return f'id:{self.id}--name:{self.username}'  # 注此处的是点不是逗号
