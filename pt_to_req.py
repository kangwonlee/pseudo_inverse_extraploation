# -*- coding: utf8 -*-

from table_to_csv import read_txt_lines
from match_table import str_list_to_string


def main(match_filename):
    lines = read_txt_lines(match_filename, 'utf8')
    print(str_list_to_string(lines))


if __name__ == '__main__':

    import sys

    if 2 == len(sys.argv):
        main(sys.argv[1])
