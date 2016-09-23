# -*- coding: cp949 -*-
from table_to_csv import read_txt_lines


def main(req_filename, table_filename):
    req_lines, table_lines = read_txt_lines(req_filename), read_txt_lines(table_filename, 'utf8')

    for req_line in req_lines:
        print(req_line)

    for table_line in table_lines:
        print(table_line)


if __name__ == '__main__':
    import sys
    if 3 == len(sys.argv):
        main(sys.argv[1], sys.argv[2])
