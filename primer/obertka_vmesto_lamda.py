def get_status(a, b, c):
    """

    :param a:
    :param b:
    :param c:
    :return:
    """
    return a+b+c


def fun(a, b, c):
    """
    обертка которая как и лямбда вернет объект но запомнить последнее значение по вызову fun.result
    """

    def xxx():
        y = get_status(a, b, c)
        xxx.result = y
        return y

    return xxx


я = fun.result


def fun2(a, b, c):
    """ обертка которая может заменить лямбду"""
    def xxx():
        return get_status(a, b, c)
    return xxx


fun3 = lambda a, b, c: get_status(a, b, c)


a=0
b=2
c=4
def fun4():
    """ обертка которая не приниммает новых значений"""
    return get_status(a, b, c)

