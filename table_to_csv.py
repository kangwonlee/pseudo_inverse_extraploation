# -*- coding: cp949 -*-
import io


def main(filename):
    # http://stackoverflow.com/questions/25049962/is-encoding-is-an-invalid-keyword-error-inevitable-in-python-2-x
    fp = io.open(filename, 'rt', encoding='cp949')
    txt_lines = fp.readlines()
    process_lines(txt_lines)


def process_lines(txt_lines):
    # line loop
    for line in txt_lines:
        process_line(line)


def process_line(txt):
    print(txt)


if __name__ == '__main__':
    import sys
    if 2 == len(sys.argv):
        main(sys.argv[1])
