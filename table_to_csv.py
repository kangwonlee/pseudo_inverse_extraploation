# -*- coding: cp949 -*-


def main(filename):
    with open(filename, 'rt') as fp:
        txt_lines = fp.readlines()
    process_lines(txt_lines)


def process_lines(txt_lines):
    for line in txt_lines:
        process_line(line)


def process_line(txt):
    print(txt)


if __name__ == '__main__':
    import sys
    if 2 == len(sys.argv):
        main(sys.argv[1])
