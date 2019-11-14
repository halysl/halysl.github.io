# -*- coding: utf-8 -*-
import re
from pathlib import Path

base_path = Path(__file__).absolute().parent
post_name_path = base_path.joinpath('post_name')
all_md_file_path = base_path.cwd().glob('*.md')

all_md_file_name = [i.name for i in all_md_file_path]
all_md_file_name = sorted(filter(lambda x: re.match(r"\d{4}-\d{2}-\d{2}-.*.md", x), all_md_file_name))

with open(post_name_path, 'w') as f:
    count = 0
    for file_name in all_md_file_name:
            count += 1
            f.write(file_name)
            f.write("\n")
    f.write(f"\n总计有{count}篇文章")
