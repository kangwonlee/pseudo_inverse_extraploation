# -*- coding: utf8 -*-
import difflib

import pandas

from MyPrettyPrinter import MyPrettyPrinter

mpp = MyPrettyPrinter(width=2075)
TAB = chr(9)


def main(req_filename, point_filename):
    # read files
    req_table = read_req_table(req_filename)
    point_table = read_point_table(point_filename)

    # calculate match
    # TODO : revise for pandas
    match_table = build_match_table(req_table, point_table)
    print_match_table(match_table, point_table)


def read_req_table(req_filename):
    req_table = pandas.read_table(req_filename, delimiter=TAB, encoding='cp949', names=(
        'name', 'req', 'agreement', 'delta',))
    return req_table


def read_point_table(point_filename):
    point_table = pandas.read_table(point_filename, delimiter=TAB, encoding='utf8', names=(
        'number', 'type', 'name', 'PO1', 'PO2', 'PO3', 'PO4', 'PO5', 'PO6', 'PO7', 'PO8',))
    return point_table


def build_match_table(req_table, point_table):
    req_names = req_table['name']
    point_names = point_table['name']

    # http://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-then-filling-it
    match_table = pandas.DataFrame(index=point_names, columns=req_names)

    for req_key in req_names:
        s = match_table[req_key]
        for point_key in point_names:
            s[point_key] = similar(req_key, point_key)

    print("match_table.shape = %s" % str(match_table.shape))

    for row in match_table.values:
        print('row '.ljust(40, '*'))
        print(row)
        print("row.shape = %s" % str(row.shape))
        print('end row '.ljust(40, '*'))

    print('begin match table '.ljust(60, '='))
    print(match_table)
    print('end match table '.ljust(60, '='))

    return match_table


def get_point_table_name_key(point_lines):
    result = {}
    for point_line in point_lines:
        point_row_list = get_row_list(point_line)
        result[point_row_list[2]] = {
            'number': point_row_list[0],
            'points': point_row_list[3:],
        }
        # print(str_list_to_string(point_row_list))

    return result


def print_match_table(match_table, point_table):
    for req_key, value in match_table.iteritems():
        # mpp.pprint((req_key, value, point_table[req_key]))
        mpp.pprint((req_key, value))


def similar(string_a, string_b):
    # http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
    return difflib.SequenceMatcher(None, string_a, string_b).ratio()


def get_point_table_number_key(point_lines):
    result = {}
    for point_line in point_lines:
        point_row_list = get_row_list(point_line)
        result[point_row_list[0]] = {
            'name': point_row_list[2],
            'points': point_row_list[3:],
        }
        # print(str_list_to_string(point_row_list))

    return result


def get_req_table(req_lines):
    result = {}
    for req_line in req_lines:
        req_row_list = get_row_list(req_line)
        result[req_row_list[0]] = req_row_list[1:]
        # print(str_list_to_string(req_row_list))

    return result


def wrap_quote(item):
    format_string = get_quote_format_string(item)
    return format_string % item


def get_quote_format_string(item):
    if ("'" not in item) and ('"' not in item):
        format_string = "'%s'"
    elif ("'" in item) and ('"' not in item):
        format_string = '"%s"'
    elif ("'" not in item) and ('"' in item):
        format_string = "'%s'"
    elif ("'" in item) and ('"' in item):
        format_string = """'''%s'''"""
    else:
        die('impossible quote mark')
    return format_string


def table_dict_list_to_string(table_dict, new_line=chr(10)):
    def k_v_to_string(k_v):
        key_string, line_list = k_v
        return "%s: %s," % (wrap_quote(key_string), line_list)

    # convert key value pair to string
    result_list = map(k_v_to_string, table_dict.iteritems())

    # opening and closing of dictionary
    result_list.insert(0, '{')
    result_list.append('}')

    # assemble result text
    result_txt = new_line.join(result_list)

    return result_txt


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
