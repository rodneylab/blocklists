#!/usr/local/bin/python3 -tt
# -*- coding: utf-8 -*-
from netaddr import cidr_merge, IPNetwork, IPSet, iter_iprange
import re
import urllib.request
import yaml


def download_lists(lists):
    for item in lists:
        urllib.request.urlretrieve(
            item['url'], get_list_filename(item['name']))


def get_list_filename(name):
    path = './downloaded/' + to_kebab_case(name).replace('.', '-')
    return path


def get_martians():
    result = ['192.168.0.0',
              '10.0.0.0',
              '172.16.0.0',
              '127.0.0.0',
              '0.0.0.0']
    return result


def get_cidr_list_from_range_list(file_path):
    input_file = open(file_path, 'r')
    cidr_list = []
    regex = re.compile(r'(?<![\.\d])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:\/[0-9])?')
    for line in input_file:
        matches = re.findall(regex, line)
        if matches:
            range = list(iter_iprange(matches[0], matches[1]))
            for cidr in cidr_merge(range):
                cidr_list.append(cidr)
    return cidr_merge(cidr_list)


def get_cidr_list_from_ip_list(file_path, martians):
    input_file = open(file_path, 'r')
    cidr_list = []
    regex = re.compile(
        r'(?<![\.\d])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:\/[0-9]{1,2})?')
    for line in input_file:
        matches = re.findall(regex, line)
        for match in matches:
            if not str(IPNetwork(match).ip) in martians:
                cidr_list.append(IPNetwork(match))
    return cidr_merge(cidr_list)


def get_ipset_intersection_size(ipset_1, ipset_2):
    intersection = ipset_1 & ipset_2
    return len(intersection)


def load_lists():
    with open(r'./lists.yml') as file:
        lists = yaml.load(file, Loader=yaml.FullLoader)
    return lists['lists']


def get_ipsets(lists, martians):
    result = []
    for item in lists:
        name = item['name']
        cidr_list = []
        if item['format'] == 'range':
            cidr_list = get_cidr_list_from_range_list(get_list_filename(name))
        else:
            cidr_list = get_cidr_list_from_ip_list(
                get_list_filename(name), martians)
        result.append({
            'name': name,
            'ipset': IPSet(cidr_list)
        })
    return result


def print_intersection_matrix(ipsets):
    for item_1 in ipsets:
        for item_2 in ipsets:
            print(
                item_1['name'],
                item_2['name'],
                get_ipset_intersection_size(item_1['ipset'], item_2['ipset'])
            )


def print_list_stats(ipsets):
    for item in ipsets:
        print(item['name'], len(item['ipset'].iter_cidrs()),  len(item['ipset']))


def to_kebab_case(value):
    return '-'.join(value.lower().split())


def main():
    lists = load_lists()

    download_lists(lists)

    martians = get_martians()

    ipsets = get_ipsets(lists, martians)
    print_list_stats(ipsets)

    print_intersection_matrix(ipsets)


if __name__ == '__main__':
    main()
