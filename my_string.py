# -*- coding: cp949 -*-
# TODO : Make repr of container objects with Korean characters more readable


class MyStr(unicode):
    def __repr__(self):
        repr_sample = super(MyStr, self).__repr__().strip('u')
        if repr_sample.startswith('"""'):
            quote_string = '"""'
        elif repr_sample.startswith("'''"):
            quote_string = "'''"
        elif repr_sample.startswith('"'):
            quote_string = '"'
        elif repr_sample.startswith("'"):
            quote_string = "'"
        else:
            print("unable to decide quote string")
            assert False
        return '%s%s%s' % (quote_string, self, quote_string)


def die(reason):
    import sys
    print(reason)
    sys.exit(-1)
