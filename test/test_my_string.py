# -*- coding: cp949 -*-
import unittest

import my_string


class TestMyString(unittest.TestCase):
    def test_repr(self):
        s = my_string.MyStr('������', encoding='cp949')
        print (s)
        print (s[0])
        repr_sample = super(my_string.MyStr, s).__repr__().strip('u')

        print (repr_sample)
        result = repr(s)
        self.assertEqual("'������'", result)


if __name__ == '__main__':
    unittest.main()
