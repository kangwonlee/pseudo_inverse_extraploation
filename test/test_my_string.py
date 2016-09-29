# -*- coding: cp949 -*-
import unittest

import my_string


class TestMyString(unittest.TestCase):
    def test_repr(self):
        s = my_string.MyStr('가나다', encoding='cp949')
        result = repr(s)
        self.assertEqual("'가나다'", result)


if __name__ == '__main__':
    unittest.main()
