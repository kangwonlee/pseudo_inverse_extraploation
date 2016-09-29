# -*- coding: utf8 -*-
# TODO : Make repr of container objects with Korean characters more readable


class my_str(unicode):
    def __repr__(self):
        repr_sample = super(my_str, self).__repr__()
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
        return quote_string + super(my_str, self).__str__() + quote_string


def die(reason):
    import sys
    print(reason)
    sys.exit(-1)
