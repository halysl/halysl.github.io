#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: 
# Desc: 
# Author: 刘志
# Email: halysl0817@gmail.com
# HomePage: ${link}
# Version: 0.0.1
# LastChange: 2018-11-28 15:24
# History:
# slogan: 狂风骤雨催纸伞，游人浪迹步不休，天地滂沱如何渡，蓑衣褪尽任浊流。
#=============================================================================
"""
import os
import commands
import logging

logger = logging.getLogger('update api doc')
logger.setLevel(logging.INFO)

try:
    src_path = os.path.join('/root', 'doc', 'ci-web-service')
    dst_path = os.path.join('/root', 'doc', 'ci-web-service-doc')
    logging.info('src path: {0} dst path: {1}'.format(src_path, dst_path))
    os.chdir(src_path)
    status, out = commands.getstatusoutput('git pull')
    logging.info('git pull status: {0}, out: {1}'.format(status, out))
    status, out = commands.getstatusoutput('apidoc -i web_service/ -o {}'.format(dst_path))
    logging.info('update apidoc status: {0}, out: {1}'.format(status, out))
    print('Done!')
except Exception as e:
    raise e
