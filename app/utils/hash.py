from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

s = Serializer("dfnsdkgnkdfg")

def encryption(info):
    """
    生成token
    :param api_user:用户id
    :return: token
    """

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    # 接收用户id转换与编码
    token = s.dumps(info)
    return token

def decrypt(info):
    return s.loads(info)
if __name__ == '__main__':
    pass