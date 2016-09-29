# -*- coding: utf8 -*-
import re

import numpy

import match_table
from MyPrettyPrinter import MyPrettyPrinter
from table_to_csv import read_txt_lines

mpp = MyPrettyPrinter()
TAB, CR = chr(9), chr(10)


def main(match_filename, feature_filename, label_filename):
    # read and prepare matching data
    lines = read_txt_lines(match_filename, 'utf8')
    tab_separated_lines = tab_separate(lines)
    transposed_table = match_table_to_dict(tab_separated_lines)

    # read & prepare feature and label tables
    feature_table = match_table.read_point_table(feature_filename, match_table.get_point_table_number_key)
    label_table = match_table.read_req_table(label_filename)

    # associate selected features and labels
    selected_dict = join_features_labels(feature_table, label_table, transposed_table)

    bias, name_list, number_list, w_list, y_hat_mat = linear_estimator(selected_dict)

    formatter = TAB.join(['%s', '%s', '%g'])

    print('selected estimation'.ljust(60, '*'))
    for number, name, y_hat in zip(number_list, name_list, y_hat_mat.tolist()):
        print(formatter % (number, name, y_hat[0]))
    print('end selected estimation'.ljust(60, '*'))

    print(w_list)

    apply_estimate(feature_table, w_list, bias)


def linear_estimator(selected_dict):
    # feature and label arrays
    number_list, feature_list, label_list, name_list = [], [], [], []
    for number in selected_dict.iterkeys():
        number_list.append(number)
        feature_list.append(selected_dict[number]['feature'])
        label_list.append(selected_dict[number]['label'])
        name_list.append(selected_dict[number]['name'])
    feature_array = numpy.array(feature_list)
    label_array = numpy.array(label_list)

    formatter = TAB.join(['%s', '%s', '%r'])

    print('selected label'.ljust(60, '*'))
    for number, name, label in zip(number_list, name_list, label_list):
        print(formatter % (number, name, label))
    print('end selected label'.ljust(60, '*'))

    print(feature_array)
    print(label_array)
    print(feature_array.shape)
    print(label_array.shape)
    w_list, bias = get_param(feature_array, label_array)
    y_hat_mat = estimate(feature_array, w_list, bias)
    return bias, name_list, number_list, w_list, y_hat_mat


def get_field_array(selected_dict, field_name):
    return numpy.array(get_field(selected_dict, field_name))


def apply_estimate(feature_table, weight, bias):
    mpp.pprint(feature_table)

    feature_list, number_list, name_list = [], [], []

    for number in feature_table.iterkeys():
        number_list.append(number)
        name_list.append(feature_table[number]['name'])
        feature_list.append(feature_table[number]['points'])

    feature_mat = numpy.matrix(feature_list, dtype=float)

    w_mat = numpy.matrix(weight)

    y_hat_mat = feature_mat * w_mat + bias
    print(feature_mat.shape)
    print(w_mat.shape)
    print(y_hat_mat.shape)

    formatter = TAB.join(('%s', '%s', '%g'))

    for number, name, y_hat in zip(number_list, name_list, y_hat_mat.tolist()):
        print(formatter % (number, name, y_hat[0]))

    return y_hat_mat


def estimate(feature_rows, weight, bias):
    feature_mat = numpy.matrix(feature_rows)
    w_mat = numpy.matrix(weight)

    return feature_mat * w_mat + bias


def get_param(feature_array, label_array):
    """
    model : y_(nx1) = X_(nxm) w_(mx1)
    (X' X)_inv X' y_(nx1) = (X' X)_inv X' X w_(mx1)
    w_(mx1) = (X' X)_inv X' y_(nx1)

    :param feature_array:
    :param label_array:
    :return:
    """
    # add a column of 1 for bias
    feature_1_array = numpy.concatenate((feature_array, numpy.ones((feature_array.shape[0], 1))), axis=1)
    print(feature_1_array.shape)

    feature_1_mat = numpy.matrix(feature_1_array)
    label_mat = numpy.matrix(label_array).T
    xt_x = feature_1_mat.T * feature_1_array
    xt_x_inv = xt_x.I
    expect_identity = xt_x_inv * xt_x
    left_inv = xt_x_inv * feature_1_mat.T
    w_1 = left_inv * label_mat
    w_1_list = w_1.tolist()
    w_list = w_1_list[:-1]
    bias = w_1_list[-1]

    return w_list, bias


def get_field(selected_dict, key):
    def dict_get(dictionary):
        return dictionary.get(key, None)

    return map(dict_get, selected_dict.itervalues())


def join_features_labels(feature_table, label_table, transposed_table):
    selected_dict = {}
    for selected_k_v in transposed_table.iteritems():
        key_label = selected_k_v[0]
        bind_info = selected_k_v[1]
        selected_dict[key_label] = {
            'name': feature_table[key_label]['name'],
            'feature': map(float, feature_table[key_label]['points']),
            'label': float(label_table[bind_info['req_key'].strip()][0])}
        print(match_table.table_dict_list_to_string(selected_dict[key_label], new_line=' '))

    return selected_dict


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
        return ': '.join([match_table.wrap_quote(k_v[0]), k_v[1]])

    key = tuple_key_dict[0]
    dict = tuple_key_dict[1]

    result_list = map(key_value_to_string, dict.iteritems())

    dict_string = ', '.join(result_list)

    result_string = '{%s: {%s}}' % (match_table.wrap_quote(key), dict_string)

    return result_string


def dict_dict_to_string(dict_dict):
    result_list = map(dict_to_string, dict_dict.iteritems())

    result_list.insert(0, '[')
    result_list.append(']')

    return CR.join(result_list)


if __name__ == '__main__':

    import sys

    if 4 == len(sys.argv):
        main(sys.argv[1], sys.argv[2], sys.argv[3])
