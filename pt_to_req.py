# -*- coding: utf8 -*-
import re

from match_table import str_list_to_string, wrap_quote
from table_to_csv import read_txt_lines

TAB = chr(9)
CR = chr(10)


def main(match_filename):
    lines = read_txt_lines(match_filename, 'utf8')
    
    tab_separated_lines = tab_separate(lines)

    for tab_sep_line in tab_separated_lines:
        print(str_list_to_string(tab_sep_line))

    transposed_table = match_table_to_dict(tab_separated_lines)
    print_dict_dict(transposed_table)


def match_table_to_dict(tab_separated_lines):
    def join_comma_space_re_group_map_helper(items):
        return ', '.join(items[0])

    def found_to_dict(found):
        return {'name': found[0], 'number': found[1], 'point': found[2]}

    result = {}

    point_search = re.compile(r'(.+)\s\((.+)\)\s=\s(.+)')

    for tab_sep_line in tab_separated_lines:
        req_key = tab_sep_line[0]
        pt_string_list = tab_sep_line[1:]
        pt_list_list_tuple = map(point_search.findall, pt_string_list)

        for pt_list_tuple in pt_list_list_tuple:
            result[pt_list_tuple[0][1]] = {'req_key': req_key,
                                           'name': pt_list_tuple[0][0],
                                           'point': pt_list_tuple[0][2]}

    return result


def tab_separate(lines_list):
    result = []
    for line in lines_list:
        result.append(line.strip().split(TAB))

    return result


def print_dict_dict(dict_dict):
    print(dict_dict_to_string(dict_dict))


def dict_to_string(tuple_key_dict):
    def key_value_to_string(k_v):
        return ': '.join([wrap_quote(k_v[0]), k_v[1]])

    key = tuple_key_dict[0]
    dict = tuple_key_dict[1]

    result_list = map(key_value_to_string, dict.iteritems())

    dict_string = ', '.join(result_list)

    result_string = '{%s: {%s}}' % (wrap_quote(key), dict_string)

    return result_string


def dict_dict_to_string(dict_dict):
    result_list = map(dict_to_string, dict_dict.iteritems())

    result_list.insert(0, '[')
    result_list.append(']')

    return CR.join(result_list)


if __name__ == '__main__':

    import sys

    if 2 == len(sys.argv):
        main(sys.argv[1])
