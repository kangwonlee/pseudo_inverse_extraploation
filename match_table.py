# -*- coding: utf8 -*-
import difflib

from table_to_csv import read_txt_lines

TAB = chr(9)


def main(req_filename, point_filename):
    # read files
    req_lines = read_txt_lines(req_filename)
    point_lines = read_txt_lines(point_filename, 'utf8')

    # convert to tables
    req_table = get_req_table(req_lines)
    print_dict_list(req_table)

    point_table = get_point_table(point_lines)

    # calculate match
    match_table = build_match_table(req_table, point_table)
    print_match_table(match_table, point_table)


def print_match_table(match_table, point_table):
    for req_key, value in match_table.iteritems():
        line_string = make_match_table_row_string(req_key, value, point_table)
        print(line_string)



def make_match_table_row_string(req_key, point_list, point_table):
    point_list_item_string_list = []
    for point_list_item in point_list:
        point_list_item_string_list.append(make_point_list_item_string(point_list_item, point_table))

    point_list_item_string = (TAB + ' ').join(point_list_item_string_list)

    line_string = '%s %s %s' % (req_key, TAB, point_list_item_string)
    return line_string


def make_point_list_item_string(point_list_item, point_table):
    point_key = point_list_item[1]
    similarity_point = point_list_item[0]
    number = point_table[point_key]['number']
    point_list_item_string = '%s (%s) = %4.2g' % (point_key, number, similarity_point)
    return point_list_item_string


def build_match_table(req_table, point_table):
    result = {}
    req_keys = req_table.keys()
    point_keys = point_table.keys()

    for req_key in req_keys:
        row_result = []
        for point_key in point_keys:
            row_result.append((similar(req_key, point_key), point_key))
        row_result.sort()
        row_result.reverse()
        result[req_key] = row_result

    return result


def print_dict_list(dict):
    print(table_dict_list_to_string(dict))


def similar(string_a, string_b):
    # http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
    return difflib.SequenceMatcher(None, string_a, string_b).ratio()


def get_point_table(point_lines):
    result = {}
    for point_line in point_lines:
        point_row_list = get_row_list(point_line)
        result[point_row_list[2]] = {
            'number': point_row_list[0],
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


def table_dict_list_to_string(table_dict):
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
