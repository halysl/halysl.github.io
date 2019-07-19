# -*- coding: utf-8 -*-
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir_path, 'post_name'), 'w') as f:
    for file_name in os.listdir(dir_path):
        if not os.path.isdir(file_name) and "md" in file_name:
            f.write(file_name)
            f.write("\n")
