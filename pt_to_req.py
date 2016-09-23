# -*- coding: utf8 -*-

from table_to_csv import read_txt_lines
from match_table import str_list_to_string

TAB = chr(9)


def main(match_filename):
    # read file
    lines = read_txt_lines(match_filename, 'utf8')
    tab_separated_lines = tab_separate(lines)

    for tab_sep_line in tab_separated_lines:
        print(str_list_to_string(tab_sep_line))


def tab_separate(lines_list):
    result = []
    for line in lines_list:
        result.append(line.strip().split(TAB))

    return result


if __name__ == '__main__':

    import sys

    if 2 == len(sys.argv):
        main(sys.argv[1])
