#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser("log parser")
parser.add_argument('log_file', help="file need to be processed.", type=str)
args = parser.parse_args()

flag_set = {'model train finish:', 'valid yun metric:', '---train finish ---', 'Class weights', 'one_hot', 'sum_prob'}
remain_list = []
with open(args.log_file) as f:
    for line in f:
        for flag in flag_set:
            if flag in line:
                remain_list.append(line)

with open(args.log_file+'.remain', 'w') as f:
    f.write("".join(remain_list))
print("process finish...")
