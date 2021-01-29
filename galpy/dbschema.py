from pathlib import Path
import pkg_resources
import logging
from .dbconnect import DatabaseCreate, DbNames, Database
_logger = logging.getLogger("galpy.dbschema")


def database_schema(db_config):

    schema = UploadSchema(db_config)
    schema_existence = schema.check_schema_existence()

    if not schema_existence:
        _logger.debug('Uploading Database Scheme : Processing')

        schema.upload_shared_resource_schema()
        _logger.debug('Shared resource Schema upload complete')

        schema.upload_dots_schema()
        _logger.debug('DOTS Schema upload complete')

        schema.add_database_constrain()
        _logger.debug('Uploading Database Scheme : Complete')
    else:
        _logger.debug('Database Schema already exist')


class DefaultSchemaPath:
    def __init__(self):
        sres_schema = "SRes.sql"
        dots_schema = "DoTS.sql"

        self.schema_path = pkg_resources.resource_filename('galpy', 'data', 'DbSchema')
        self.sres_schema_path = Path(self.schema_path).joinpath(sres_schema)
        self.dots_schema_path = Path(self.schema_path).joinpath(dots_schema)


class UploadSchema(DefaultSchemaPath):
    def __init__(self, db_config):
        DefaultSchemaPath.__init__(self)

        self.db = DatabaseCreate(db_config.host, db_config.db_username, db_config.db_password)
        self.db_name = DbNames(db_config.db_prefix)

        self.core = self.db.create(self.db_name.core)
        self.dots = self.db.create(self.db_name.dots)
        self.shared_resource = self.db.create(self.db_name.sres)

        self.db_dots = Database(db_config.host, db_config.db_username, db_config.db_password, self.db_name.dots, 0)
        self.db_shared_resource = Database(db_config.host, db_config.db_username, db_config.db_password,
                                           self.db_name.sres, 0)

    def check_schema_existence(self):
        sql_tax = "SELECT * FROM {}.GeneticCode;".format(self.db_name.sres)
        row_tax = self.db.rowcount(sql_tax)
        if row_tax is None:
            return False
        else:
            return True

    def upload_shared_resource_schema(self):
        if self.sres_schema_path:
            upload_schema_based_on_line(self.sres_schema_path, self.db_shared_resource)
        else:
            _logger.error("File not found: {}".format(self.sres_schema_path))

    def upload_dots_schema(self):

        if self.dots_schema_path.exists():
            upload_schema_based_on_line(self.dots_schema_path, self.db_dots)
        else:
            _logger.error("File not found: {}".format(self.dots_schema_path))

    def add_database_constrain(self):
        organism_table = self.db_name.dots + ".Organism"
        taxonomy_table = self.db_name.sres + ".Taxon"

        organism_constrain_query = """ALTER TABLE {} ADD FOREIGN KEY (TAXON_ID) REFERENCES {}(NCBI_TAXON_ID);""".format(
            organism_table, taxonomy_table)

        self.db_dots.query(organism_constrain_query)


def upload_schema_based_on_line(filename, db):
    try:
        with open(filename, 'r') as FH:
            query = " ".join(FH.readlines())
            query_array = query.split(';')
            for line, each_query in enumerate(query_array[:-1]):
                if each_query:
                    db.insert(each_query)

    except (OSError, ValueError, TypeError) as e:
        _logger.error("Schema upload has issue: {}".format(filename))
        _logger.error("Error: {}".format(e))

