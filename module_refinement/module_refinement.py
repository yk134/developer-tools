# -*- coding: utf-8 -*-
# !/usr/bin/python

import os
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
)

_help='''#######################################################################################################
Run command  : python module_refinement.py <path> [--help/-h]

@param -> module_refinement.py : to check few required files and folders in module
@param -> <path>         : give a path where your module is located

@example> For Help       : python module_refinement.py [-h]
@example> Without Copy   : python module_refinement.py ~/mymodule
#######################################################################################################'''

if '--help' in sys.argv or '-H' in sys.argv or '-h' in sys.argv:
    print(_help)
    os._exit(1)

if len(sys.argv) < 2:
    logging.error('Directory path is required, pelase follow below instructions.')
    print(_help)
    os._exit(1)
else:
    dir_path = sys.argv[1]
    if not os.path.isdir(dir_path) and not os.path.exists(dir_path):
        logging.error('Directory does not exist. Please check for path : %s' % dir_path)
        print(_help)
        os._exit(1)

suffix = "/"
while dir_path.endswith(suffix,len(dir_path)-1) :
    dir_path = dir_path[:len(dir_path)-1]
module_name = dir_path.split('/')[-1]

required_folders = [
    "i18n",
    "security",
    "tests",
    "demo",
]

required_files = [
    "i18n/"+module_name+".pot",
    "security/ir.model.access.csv",
]

optional_files = [
    "README.MD",
]

optional_folders = {
    "doc",
    "data",
    "report",
    "static"
}

manifest_keys = [
    'category',
    'version',
    'website',
    'depends',
    'description',
    'summery',
    'author',
]

check_errors = 0

def check_manifest():
    logging.info("__MANIFEST__.PY.")
    logging.info("************************************************************")
    logging.info("Following key must be defined in __manifest__.py :")
    try:
        with open(dir_path + '/__manifest__.py', 'r') as file:
            global check_errors
            data = eval(file.read())
            for key in manifest_keys:
                val = data.get(key, "<NOT FOUND>")
                _info = "%-12s: %s" %(key, val)
                flags=(check_errors + 1, logging.error) if val is "<NOT FOUND>" else (check_errors, logging.info)
                check_errors = flags[0] 
                flags[1](_info)
    except Exception as e:
        logging.error('Please check for __manifest__.py file')

def check_requirements(requirements, _dirs=True, _optional=False):
    logging.info("Required Folders With Its Files.")
    logging.info("************************************************************")
    logging.info("Few files must be in your module check for it :")
    global check_errors
    check = os.path.isdir if _dirs else os.path.isfile
    display = logging.info if _optional else logging.error
    for _dir in requirements:
        if os.path.exists(dir_path+'/'+_dir) and check(dir_path+'/'+_dir):
            logging.info("%s/%s exists..."%(dir_path, _dir))
            if _dirs:
                if not os.listdir(dir_path+'/'+_dir):
                    display("%s/%s is empty..."%(dir_path, _dir))
                    check_errors += 1
        else:
            display("%s/%s does not exist. %s"%(dir_path, _dir, '(optional)' if _optional else ''))
            if not _optional:
                check_errors += 1

check_manifest()
check_requirements(required_folders, True, False)
check_requirements(required_files, False, False)
check_requirements(optional_folders, True, True)
check_requirements(optional_files, False, True)

logging.info(check_errors)
