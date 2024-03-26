import argparse
import logging
import pkg_resources
from pathlib import Path
from .app import App, BaseApp, OrganismApp


def main():
    """
    galEupy main command line
    """
    print("Welcome to galEupy")

    default_data_path = pkg_resources.resource_filename('galEupy', 'data')
    default_config_path = Path(default_data_path).joinpath('DefaultConfig')

    default_db_config = default_config_path.joinpath('database.ini')
    default_path_config = default_config_path.joinpath('path.ini')
    default_org_config = default_config_path.joinpath('organism_config_format.ini')

    parser = argparse.ArgumentParser()
    parser.add_argument("-db", "--dbconfig", help='Database configuration file name', default=default_db_config)
    parser.add_argument("-path", "--pathconfig", help='path configuration file name', default=default_path_config)
    parser.add_argument("-org", "--orgconfig", help='Organism configuration file name', default=default_org_config)

    parser.add_argument('-upload', '--upload', type=str.lower, choices=["all", "centraldogma", "proteinannotation"],
                        help="Upload data using different levels")

    parser.add_argument("-info", "--info", type=str2bool, nargs='?', const=True, default=False,
                        help='Gives information of the table status')
    parser.add_argument("-org_info", "--org_info", type=str2bool, nargs='?', const=True, default=False,
                        help="Gives information of an organism's upload status")
    parser.add_argument("-remove_org", "--remove_org", type=str2bool, nargs='?', const=True, default=False,
                        help='Removes an organism details from the database')
    parser.add_argument("-remove_db", "--remove_db", type=str2bool, nargs='?', const=True, default=False,
                        help='Removes the entire GAL related databases')

    parser.add_argument('-v', '--verbose', type=str, default="info",
                        choices=["none", "debug", "info", "warning", "error", "d", "e", "i", "w"],
                        help="verbose level: debug, info (default), warning, error" )
    parser.add_argument('-log', '--log_file', type=str, help='log file')
    args = parser.parse_args()

    db_config_file = args.dbconfig
    path_config_file = args.pathconfig
    org_config_file = args.orgconfig

    logger = get_logger(args)

    logger.debug("Start logging...")
    logger.debug(f"""Path for configuration files:
    DB Config: {db_config_file}
    Path Config: {path_config_file}
    Organism Config: {org_config_file}""")

    if args.info:
        base_app_obj = BaseApp(db_config_file)
        if base_app_obj.db_status:
            base_app_obj.db_schema()

    elif args.remove_db:
        base_app_obj = BaseApp(db_config_file)
        if base_app_obj.db_status:
            base_app_obj.drop_databases()

    elif args.org_info:
        org_app_obj = OrganismApp(db_config_file, org_config_file)
        org_app_obj.db_table_log()
        org_app_obj.get_organism_record()

    elif args.remove_org:
        org_app_obj = OrganismApp(db_config_file, org_config_file)
        org_app_obj.db_table_log()
        org_app_obj.remove_organism_record()

    if args.upload:
        if args.upload == 'all':
            app = App(db_config_file, path_config_file, org_config_file)
            app.upload_schema()
            app.process_central_dogma_annotation()
            app.import_protein_annotation()
            logger.info("Table max ids after the upload")
            app.db_table_logs()

        elif args.upload == 'centraldogma':
            app = App(db_config_file, path_config_file, org_config_file)
            app.upload_schema()
            app.process_central_dogma_annotation()
            logger.info("Table max ids after the upload")
            app.db_table_logs()

        elif args.upload == 'proteinannotation':
            app = App(db_config_file, path_config_file, org_config_file)
            app.upload_schema()
            app.import_protein_annotation()
            logger.info("Table max ids after the upload")
            app.db_table_logs()


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
        logger = logging.getLogger('galEupy')
        ch = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        ch.setFormatter(formatter)
        ch.setLevel(level)
        logger.addHandler(ch)
    else:
        logging.basicConfig(level=level, format=log_format)
        logger = logging.getLogger('galEupy')

    return logger


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
