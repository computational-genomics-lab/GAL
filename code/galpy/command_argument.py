import os
import argparse
from pathlib import Path, PurePosixPath, PurePath


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class ProcessArguments:
    def __init__(self, content_dir):
        default_db_config_file = 'config/database.ini'
        default_path_config_file = 'config/path.ini'
        default_organism_file = 'config/set1/type1/case1.Ini'
        default_log_file = 'gal.log'
        default_new_upload = True

        default_db_config = PurePosixPath(content_dir, default_db_config_file)
        default_path_config = PurePosixPath(content_dir, default_path_config_file)

        default_org_config = PurePosixPath(content_dir, default_organism_file)

        default_log = PurePosixPath(content_dir, default_log_file)

        command_line_argument_parser = argparse.ArgumentParser()
        command_line_argument_parser.add_argument("-db", "--dbconfig", help='Database configuration file name',
                                                  default=default_db_config)
        command_line_argument_parser.add_argument("-path", "--pathconfig", help='path configuration file name',
                                                  default=default_path_config)
        command_line_argument_parser.add_argument("-org", "--orgconfig", help='Organism configuration file name',
                                                  default=default_org_config)
        command_line_argument_parser.add_argument("-log", "--logfile", help='Log file name', default=default_log)

        command_line_argument_parser.add_argument("-NU", "--NewUpload", help='NewUpload: True/False',
                                                  type=str2bool,
                                                  default=default_new_upload)
        command_line_arguments = command_line_argument_parser.parse_args()

        db_config_file = command_line_arguments.dbconfig
        path_config_file = command_line_arguments.pathconfig
        org_config_file = command_line_arguments.orgconfig
        log_file = command_line_arguments.logfile

        self.db_config_file = PurePosixPath(db_config_file)
        self.path_config_file = PurePosixPath(path_config_file)
        self.org_config_file = PurePosixPath(org_config_file)
        self.log_file = PurePosixPath(log_file)
        self.new_upload = command_line_arguments.NewUpload
