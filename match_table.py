# -*- coding: utf8 -*-
import difflib

from table_to_csv import read_txt_lines

TAB = chr(9)


# TODO : repr safe unicode string


def main(req_filename, point_filename):
    req_table = read_req_table(req_filename)
    print(req_table)
    point_table = read_point_table(point_filename)

    # calculate match
    match_table = build_match_table(req_table, point_table)
    print_match_table(match_table, point_table)


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


def read_point_table(point_filename, table_converter=get_point_table_name_key):
    point_lines = read_txt_lines(point_filename, 'utf8')
    point_table = table_converter(point_lines)
    return point_table


def read_req_table(req_filename):
    req_lines = read_txt_lines(req_filename)
    req_table = get_req_table(req_lines)
    return req_table


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


def str_list_to_string(str_list, sep=', '):
    result_list = map(wrap_quote, str_list)

    result_txt = sep.join(result_list)

    result_txt_bracket = '[%s]' % result_txt

    return result_txt_bracket


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
