# -*- coding: utf-8 -*-
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir_path, 'post_name'), 'w') as f:
    count = 0
    for file_name in os.listdir(dir_path):
        if not os.path.isdir(file_name) and "md" in file_name and "template" not in file_name:
            count += 1
            f.write(file_name)
            f.write("\n")
    f.write(f"\n总计有{count}篇文章")
