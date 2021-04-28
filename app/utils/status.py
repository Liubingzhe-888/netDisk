class CODE:
    """
    NOT_ALLOW = 没有登陆
    ALLOW_TODO = 允许/成功
    ERROR = 错误
    """
    ALLOW = (200, '操作被允许')
    ERROR = (301, '操作错误')
    NOT_ALLOW = (302, '操作没有被允许')
    NOT_LOGIN = (401, '未登录')
    NOT_ACCEPT = (400, '密码错误')
