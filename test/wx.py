# -*- coding:utf-8 -*-
import unittest
from research.weixin import get_wx_login


class Wx(unittest.TestCase):
    def test_error_test(self):
        res = get_wx_login(js_code='rere435')
        self.assertEquals(res.result.errcode, 40013)

    def test_ok_test(self):
        res = get_wx_login(js_code='011Rf4Su1YPy3c0NRhQu1RrURu1Rf4S4')
        self.assertTrue(res.result.get('openid'))


if __name__ == '__main__':
    unittest.main()
