# -*- coding: utf8 -*-
from table_to_csv import read_txt_lines
import sys


def main(req_filename, table_filename):
    req_lines, table_lines = read_txt_lines(req_filename), read_txt_lines(table_filename, 'utf8')

    get_req_table(req_lines)

    for table_line in table_lines:
        print(table_line)


def get_req_table(req_lines):
    result = {}
    for req_line in req_lines:
        req_row_list = get_row_list(req_line)
        print(str_list_to_string(req_row_list))


def str_list_to_string(str_list):
    result = '['
    for item in str_list:
        if ("'" not in item) and ('"' not in item):
            format_string = "'%s', "
        elif ("'" in item) and ('"' not in item):
            format_string = '"%s", '
        elif ("'" not in item) and ('"' in item):
            format_string = "'%s', "
        elif ("'" in item) and ('"' in item):
            format_string = """'''%s''', """
        else:
            die('impossible quote mark')

        result += format_string % item

    result = result[:-1] + ']'

    return result


def get_row_list(req_line, sep='\t'):
    return req_line.strip().split(sep)


def die(reason):
    print('Something Wrong : %s' % reason)
    sys.exit(-1)


if __name__ == '__main__':
    import sys
    if 3 == len(sys.argv):
        main(sys.argv[1], sys.argv[2])
