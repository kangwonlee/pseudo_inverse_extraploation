# -*- coding: utf8 -*-
import pprint

from table_to_csv import read_txt_lines


def main(req_filename, table_filename):
    req_lines, table_lines = read_txt_lines(req_filename), read_txt_lines(table_filename, 'utf8')
    print(table_dict_to_string(get_req_table(req_lines)))

    for table_line in table_lines:
        print(table_line)


def get_req_table(req_lines):
    result = {}
    for req_line in req_lines:
        req_row_list = get_row_list(req_line)
        result[req_row_list[0]] = req_row_list[1:]
        # print(str_list_to_string(req_row_list))

    return result


def str_list_to_string(str_list):
    result = '['
    for item in str_list:
        result += wrap_quote(item)

    result = result[:-1] + ']'

    return result


def wrap_quote(item):
    format_string = get_quote_format_string(item)
    return format_string % item


def get_quote_format_string(item):
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
    return format_string


def table_dict_to_string(table_dict):
    new_line = chr(10)
    result = '{' + new_line

    for key_string, line_list in table_dict.iteritems():
        line = "%s: %s," % (wrap_quote(key_string), repr(line_list))
        result += line + new_line

    result = result[:-1]
    result += (new_line + '}')

    return result


def get_row_list(req_line, sep='\t'):
    return req_line.strip().split(sep)


def die(reason):
    import sys
    print('Something Wrong : %s' % reason)
    sys.exit(-1)


if __name__ == '__main__':
    import sys
    if 3 == len(sys.argv):
        main(sys.argv[1], sys.argv[2])
