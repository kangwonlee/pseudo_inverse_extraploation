# -*- coding: utf8 -*-
import re

from match_table import str_list_to_string
from table_to_csv import read_txt_lines

TAB = chr(9)


def main(match_filename):
    lines = read_txt_lines(match_filename, 'utf8')
    tab_separated_lines = tab_separate(lines)

    for tab_sep_line in tab_separated_lines:
        print(str_list_to_string(tab_sep_line))

    match_table_to_dict(tab_separated_lines)


def match_table_to_dict(tab_separated_lines):
    result = {}

    point_search = re.compile(r'(.+)\s\((.+)\)\s=\s(.+)')

    for tab_sep_line in tab_separated_lines:
        key = tab_sep_line[0]
        values = tab_sep_line[1:]
        result[key] = []

        for value in values:
            print(point_search.findall(value))


def tab_separate(lines_list):
    result = []
    for line in lines_list:
        result.append(line.strip().split(TAB))

    return result


if __name__ == '__main__':

    import sys

    if 2 == len(sys.argv):
        main(sys.argv[1])
