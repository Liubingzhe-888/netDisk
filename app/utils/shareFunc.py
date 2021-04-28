import uuid
import random


def get_share_password() -> str:
    """
    随机生成4位密码
    """
    strings = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    random_str = random.sample(strings, 4)
    return ''.join(random_str)


def get_uuid() -> uuid:
    """
    获取uuid
    """
    uuid_value = uuid.uuid1()
    uuid_str = uuid_value.hex
    return uuid_str
