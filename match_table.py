# -*- coding: utf8 -*-
from table_to_csv import read_txt_lines


def main(req_filename, table_filename):
    req_lines, table_lines = read_txt_lines(req_filename), read_txt_lines(table_filename, 'utf8')

    get_req_table(req_lines)

    for table_line in table_lines:
        print(table_line)


def get_req_table(req_lines):
    result = {}
    for req_line in req_lines:
        req_row_list = get_row_list(req_line)
        print(req_row_list)


def get_row_list(req_line, sep='\t'):
    return req_line.strip().split(sep)


if __name__ == '__main__':
    import sys
    if 3 == len(sys.argv):
        main(sys.argv[1], sys.argv[2])
