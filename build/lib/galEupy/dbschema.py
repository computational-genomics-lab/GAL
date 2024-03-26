from pathlib import Path
import pkg_resources
import logging
from .dbconnect import DatabaseCreate, DbNames, Database
from .commondata import DownloadCommonData, upload_shared_data
from .config_utility import DatabaseConfig
_logger = logging.getLogger("galEupy.dbschema")


def database_schema(db_config):
    _logger.debug('Checking database Schemas')
    schema = UploadSchema(db_config)
    schema_existence = schema.check_schema_existence()

    if schema_existence:
        _logger.debug('Database Schema already exist')
        return True
    else:
        _logger.debug('Uploading Database Scheme : Processing')

        schema.upload_sres_schema()
        _logger.debug('Shared resource Schema upload complete')

        schema.upload_dots_schema()
        _logger.debug('DOTS Schema upload complete')

        schema.add_database_constrain()
        _logger.debug('Uploading Database Scheme : Complete')

        _logger.debug('Uploading Shared data : Processing')
        schema.download_upload_commondata()
        _logger.debug('Uploading Shared data : Complete')

        return True


class DefaultSchemaPath:
    def __init__(self):
        sres_schema = "SRes.sql"
        dots_schema = "DoTS.sql"

        self.default_data_path = pkg_resources.resource_filename('galEupy', 'data')
        schema_path = Path(self.default_data_path).joinpath('DbSchema')

        self.sres_schema_path = schema_path.joinpath(sres_schema)
        self.dots_schema_path = schema_path.joinpath(dots_schema)


class UploadSchema(DefaultSchemaPath, DatabaseConfig):
    def __init__(self, db_config):
        """
        class constructor for Uploading schema
        parameters
        -----------
        db_config: Path
            Database configuration file
        """
        DefaultSchemaPath.__init__(self)
        DatabaseConfig.__init__(self, db_config)

        # _logger.debug('UploadSchema class initiation')
        self.db = DatabaseCreate(self.host, self.db_username, self.db_password, port=self.db_port)
        self.db_name = DbNames(self.db_prefix)

    def create_dots(self):
        # create dots db
        dots = self.db.create(self.db_name.dots)
        _logger.debug(f"Database created: {self.db_name.dots}")
        return dots

    def create_shared_resource(self):
        # creates sres database
        shared_resource = self.db.create(self.db_name.sres)
        _logger.debug(f"Database created: {self.db_name.sres}")
        return shared_resource

    @property
    def db_dots(self):
        _logger.debug("connect to db_dots database")
        db_dots = Database(self.host, self.db_username, self.db_password, self.db_name.dots, 0, port=self.db_port)
        return db_dots

    @property
    def db_sres(self):
        _logger.debug("connect to db_sres database")
        db_sres = Database(self.host, self.db_username, self.db_password, self.db_name.sres, 1, port=self.db_port)
        return db_sres

    def check_schema_existence(self):

        # _logger.debug('Checking Schema existence')
        sql_tax = "SELECT * FROM {}.GeneticCode;".format(self.db_name.sres)
        row_tax = self.db.rowcount(sql_tax)
        if row_tax is None:
            return False
        else:
            return True

    def upload_sres_schema(self):
        if self.db.db_existence(self.db_name.sres) is None:
            _logger.debug(f"Database not exist: {self.db_name.sres}")
            self.create_shared_resource()

        _logger.debug("Uploading SRES schema")

        if self.sres_schema_path.exists():
            _logger.debug(f"Schema path: {self.sres_schema_path}")
            self.upload_schema_lines(self.sres_schema_path, self.db_sres)
        else:
            _logger.error(f"File not found: {self.sres_schema_path}")

    def upload_dots_schema(self):
        if self.db.db_existence(self.db_name.dots) is None:
            _logger.debug(f"Database not exist: {self.db_name.dots}")
            self.create_dots()

        _logger.debug("Uploading DOTS schema")
        if self.dots_schema_path.exists():
            _logger.debug("Schema path: {}".format(self.dots_schema_path))
            self.upload_schema_lines(self.dots_schema_path, self.db_dots)
        else:
            _logger.error("File not found: {}".format(self.dots_schema_path))

    def add_database_constrain(self):
        organism_table = self.db_name.dots + ".Organism"
        taxonomy_table = self.db_name.sres + ".Taxon"

        organism_constrain_query = f"""ALTER TABLE {organism_table} ADD FOREIGN KEY (TAXON_ID) 
        REFERENCES {taxonomy_table}(NCBI_TAXON_ID);"""

        self.db_dots.query(organism_constrain_query)

    def download_upload_commondata(self):
        _logger.debug("Downloading common data")
        default_data_path = pkg_resources.resource_filename('galEupy', 'data')
        default_common_data_path = Path(default_data_path).joinpath('CommonData')
        download_1 = DownloadCommonData(default_common_data_path)
        download_1.download_parse_goterm_and_taxon()

        _logger.debug("Uploading common data")

        upload_shared_data(self.db_sres, default_common_data_path)
        """
        shared_data = UploadCommonData(default_common_data_path, self.db_sres)
        shared_data.upload_genetic_code()
        shared_data.upload_taxonomy_data()
        shared_data.upload_go_evidence()
        # shared_data.upload_go_term()
        shared_data.upload_gram_strain()
        """

    @staticmethod
    def upload_schema_lines(filename, db):
        _logger.debug('Processing schema line by line')
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


