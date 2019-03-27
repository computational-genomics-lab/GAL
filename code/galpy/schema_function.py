import os
import subprocess
from pathlib import Path
from galpy import db_function, gal_function, logging_utility


def database_schema(db_config, main_path, log_filename):
    logger = logging_utility.logger_function(__name__, log_filename)

    schema = UploadSchema(db_config, main_path)
    schema_existence = schema.check_schema_existence()

    if not schema_existence:
        logger.debug('Uploading Database Scheme : Processing')

        schema.upload_shared_resource_schema(logger)
        logger.debug('Shared resource Schema upload complete')

        schema.upload_dots_schema(logger)
        logger.debug('DOTS Schema upload complete')

        schema.add_database_constrain()
        logger.debug('Uploading Database Scheme : Complete')
    else:
        logger.debug('Database Schema already exist')


class DefaultSchemaPath:
    def __init__(self, content_dir):

        sres_schema = "data/Schema/SRes.sql"
        dots_schema = "data/Schema/DoTS.sql"
        self.sres_schema_path = Path(content_dir, sres_schema)
        self.dots_schema_path = Path(content_dir, dots_schema)


class UploadSchema(DefaultSchemaPath):
    def __init__(self, db_config, content_dir):
        DefaultSchemaPath.__init__(self, content_dir)

        self.db = db_function.DatabaseCreate(db_config.host, db_config.db_username, db_config.db_password)
        self.db_name = db_function.DbNames(db_config.db_prefix)

        self.core = self.db.create(self.db_name.core)
        self.dots = self.db.create(self.db_name.dots)
        self.shared_resource = self.db.create(self.db_name.sres)

        self.db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password,
                                            self.db_name.dots, 0)
        self.db_shared_resource = db_function.Database(db_config.host, db_config.db_username, db_config.db_password,
                                                       self.db_name.sres, 0)

    def check_schema_existence(self):
        sql_tax = "SELECT * FROM {}.GeneticCode;".format(self.db_name.sres)
        row_tax = self.db.rowcount(sql_tax)
        if row_tax is None:
            return False
        else:
            return True

    def upload_shared_resource_schema(self, logger):
        schema_file_existence = file_existence_check(self.sres_schema_path, logger)
        if schema_file_existence:
            upload_schema_based_on_line(self.sres_schema_path, self.db_shared_resource)

    def upload_dots_schema(self, logger):
        schema_file_existence = file_existence_check(self.dots_schema_path, logger)
        if schema_file_existence:
            upload_schema_based_on_line(self.dots_schema_path, self.db_dots)

    def add_database_constrain(self):
        organism_table = self.db_name.dots + ".Organism"
        taxonomy_table = self.db_name.sres + ".Taxon"

        organism_constrain_query = """ALTER TABLE {} ADD FOREIGN KEY (TAXON_ID) REFERENCES {}(NCBI_TAXON_ID);""".format(
            organism_table, taxonomy_table)

        self.db_dots.query(organism_constrain_query)


def file_existence_check(filename, logger):
    my_file = Path(filename)
    try:
        my_file.resolve()
        return True
    except FileNotFoundError as e:
        logger.error('FileNotFoundError: {}'.format(filename))
        raise e


def upload_schema_based_on_line(filename, db):
    try:
        with open(filename, 'r') as FH:
            query = " ".join(FH.readlines())
            query_array = query.split(';')
            for line, each_query in enumerate(query_array[:-1]):
                if each_query:
                    db.insert(each_query)

    except (OSError, ValueError, TypeError) as e:
        print("Schema upload has issue: {}".format(filename))
        print("Error: {}".format(e))

