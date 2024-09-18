import pytest
import kancolle.fe as fe


def test_fe_zh_Hans():
    expr = "CL{1,3}[0]-DD{1,}"
    assert fe.resolve(expr, 'zh_Hans') == '需要1~3个CL旗舰，需要至少1个DD，不能带其它舰种'

    expr = "CVL|CL|CLT|CT{1,}-DD|DE{3,}-ANY*"
    assert fe.resolve(expr, 'zh_Hans') == '需要至少1个CVL/CL/CLT/CT，需要至少3个DD/DE'

    expr = "BB{1}[0]-CL{1}-DD{4}"
    assert fe.resolve(expr, 'zh_Hans') == '需要1个BB旗舰，需要1个CL，需要4个DD，不能带其它舰种'

    expr = "CV|CVB{0,2}-DD{2,}"
    assert fe.resolve(expr, 'zh_Hans') == '需要至多2个CV/CVB，需要至少2个DD，不能带其它舰种'


def test_fe_zh_Hant():
    expr = "CL{1,3}[0]-DD{1,}"
    assert fe.resolve(expr, 'zh_Hant') == '需要1~3個CL旗艦，需要至少1個DD，不能帶其它艦種'

    expr = "CVL|CL|CLT|CT{1,}-DD|DE{3,}-ANY*"
    assert fe.resolve(expr, 'zh_Hant') == '需要至少1個CVL/CL/CLT/CT，需要至少3個DD/DE'

    expr = "BB{1}[0]-CL{1}-DD{4}"
    assert fe.resolve(expr, 'zh_Hant') == '需要1個BB旗艦，需要1個CL，需要4個DD，不能帶其它艦種'

    expr = "CV|CVB{0,2}-DD{2,}"
    assert fe.resolve(expr, 'zh_Hant') == '需要至多2個CV/CVB，需要至少2個DD，不能帶其它艦種'


def test_fe_ja():
    expr = "CL{1,3}[0]-DD{1,}"
    assert fe.resolve(expr, 'ja') == 'CL1~3隻必要旗艦、DD少なくとも1隻必要、他の艦種は不可'

    expr = "CVL|CL|CLT|CT{1,}-DD|DE{3,}-ANY*"
    assert fe.resolve(expr, 'ja') == 'CVL/CL/CLT/CT少なくとも1隻必要、DD/DE少なくとも3隻必要'

    expr = "BB{1}[0]-CL{1}-DD{4}"
    assert fe.resolve(expr, 'ja') == 'BB1隻必要旗艦、CL1隻必要、DD4隻必要、他の艦種は不可'

    expr = "CV|CVB{0,2}-DD{2,}"
    assert fe.resolve(expr, 'ja') == 'CV/CVB最大2隻必要、DD少なくとも2隻必要、他の艦種は不可'


def test_fe_en():
    expr = "CL{1,3}[0]-DD{1,}"
    assert fe.resolve(expr, 'en') == 'Require 1 to 3 CL as flagship, Require at least 1 DD, No other ship types allowed'

    expr = "CVL|CL|CLT|CT{1,}-DD|DE{3,}-ANY*"
    assert fe.resolve(expr, 'en') == 'Require at least 1 CVL or CL or CLT or CT, Require at least 3 DD or DE'

    expr = "BB{1}[0]-CL{1}-DD{4}"
    assert fe.resolve(expr, 'en') == 'Require exactly 1 BB as flagship, Require exactly 1 CL, Require exactly 4 DD, No other ship types allowed'

    expr = "CV|CVB{0,2}-DD{2,}"
    assert fe.resolve(expr, 'en') == 'Require up to 2 CV or CVB, Require at least 2 DD, No other ship types allowed'
