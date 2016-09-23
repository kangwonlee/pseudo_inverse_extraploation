# -*- coding: cp949 -*-
import io
import os


def main(filename):
    # http://stackoverflow.com/questions/25049962/is-encoding-is-an-invalid-keyword-error-inevitable-in-python-2-x
    fp = io.open(filename, 'rt', encoding='cp949')
    txt_lines = fp.readlines()
    fp.close()

    result = process_lines(txt_lines)

    # write to a csv file
    with io.open(get_csv_filename(filename), 'w', encoding='cp949') as wp:
        map(wp.write, result)


def get_csv_filename(filename):
    filename_split_ext = os.path.splitext(filename)
    csv_filename = filename_split_ext[0] + '.csv'
    return csv_filename


def process_lines(txt_lines):
    # line loop
    result = map(process_line, txt_lines)
    return result


def process_line(txt):
    sep = ','

    txt_strip = txt.strip()
    len_txt = len(txt)
    split_here = txt_strip.index(' ', len_txt - 18, len_txt) + 1
    name_txt = txt_strip[:split_here].strip()
    points_txt = txt_strip[split_here:].strip()
    # points_csv_txt = points_txt.replace(' ', ', ')

    points_list = map(float, points_txt.split())
    points_csv_txt = sep.join(map(str, points_list))

    return name_txt + sep + points_csv_txt + chr(10)


if __name__ == '__main__':
    import sys
    if 2 == len(sys.argv):
        main(sys.argv[1])
