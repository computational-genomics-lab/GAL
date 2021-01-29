import argparse
import logging
import pkg_resources
from pathlib import Path


def main():
    """
    galpy main command line
    """
    print("Welcome to GAL")

    default_data_path = pkg_resources.resource_filename('galpy', 'data')
    default_config_path = Path(default_data_path).joinpath('DefaultConfig')

    default_db_config = default_config_path.joinpath('database.ini')
    default_path_config = default_config_path.joinpath('organism_config_format.ini')
    default_org_config = default_config_path.joinpath('path.ini')

    parser = argparse.ArgumentParser()
    parser.add_argument("-db", "--dbconfig", help='Database configuration file name', default=default_db_config)
    parser.add_argument("-path", "--pathconfig", help='path configuration file name', default=default_path_config)
    parser.add_argument("-org", "--orgconfig", help='Organism configuration file name', default=default_org_config)
    parser.add_argument("-NU", "--NewUpload", help='NewUpload: True/False', type=str2bool, default=True)
    parser.add_argument('-v', '--verbose', type=str,
                        choices=["none", "debug", "info", "warning", "error", "d", "e", "i", "w"],
                        help="verbose level: debug, info (default), warning, error", default="info")
    parser.add_argument('-log', '--log_file', type=str, help='log file')
    args = parser.parse_args()

    db_config_file = args.dbconfig
    path_config_file = args.pathconfig
    org_config_file = args.orgconfig

    logger = get_logger(args)

    logger.debug("Start logging...")
    logger.debug("DB Config: {}".format(db_config_file))
    logger.debug("Path Config: {}".format(path_config_file))
    logger.debug("Organism Config: {}".format(org_config_file))


def get_logger(args):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if args.verbose in {"debug", "d"}:
        level = logging.DEBUG
    elif args.verbose in {"info", "i"}:
        level = logging.INFO
    elif args.verbose in {"warning", "w"}:
        level = logging.WARNING
    elif args.verbose in {"error", "e"}:
        level = logging.ERROR
    else:
        level = logging.CRITICAL

    if args.log_file:
        logging.basicConfig(filename=args.log_file, level=logging.DEBUG, format=log_format)
        logger = logging.getLogger('galpy')
        ch = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        ch.setFormatter(formatter)
        ch.setLevel(level)
        logger.addHandler(ch)
    else:
        logging.basicConfig(level=level, format=log_format)
        logger = logging.getLogger('galpy')

    return logger


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')