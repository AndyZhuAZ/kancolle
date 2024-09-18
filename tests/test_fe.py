import pytest
import kancolle.fe as fe


def test_fe():
    expr = "CL{1,3}[0]-DD{1,}"
    # 输出: 需要1~3个CL旗舰，需要至少1个DD，不能带其它舰种
    assert fe.resolve(expr, 'zh_Hans') == '需要1~3个CL旗舰，需要至少1个DD，不能带其它舰种'

    expr = "CVL|CL|CLT|CT{1,}-DD|DE{3,}-ANY*"
    # 输出: 需要至少1个CVL/CL/CLT/CT，需要至少3个DD/DE
    assert fe.resolve(expr, 'zh_Hans') == '需要至少1个CVL/CL/CLT/CT，需要至少3个DD/DE'

    expr = "BB{1}[0]-CL{1}-DD{4}"
    # 输出: 需要1个BB旗舰，需要1个CL，需要4个DD，不能带其它舰种
    assert fe.resolve(expr, 'zh_Hans') == '需要1个BB旗舰，需要1个CL，需要4个DD，不能带其它舰种'

    expr = "CV|CVB{0,2}-DD{2,}"
    # 输出: 需要至多2个CV/CVB，需要至少2个DD
    assert fe.resolve(expr, 'zh_Hans') == '需要至多2个CV/CVB，需要至少2个DD，不能带其它舰种'
