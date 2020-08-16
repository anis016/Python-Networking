import os
import logging

DEBUG = True
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def get_project_dir_name():
    project_dir, _ = os.path.split(os.path.abspath("__file__"))
    project_name = os.path.basename(project_dir)
    if DEBUG:
        logging.info("project name - {0}".format(project_name))
    return project_dir, project_name
