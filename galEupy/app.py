import sys
import logging
from pathlib import Path
from .config_utility import ConfigFileHandler, DatabaseConfig, OrganismConf
from .dbconnect import check_db_connection, Database, DatabaseCreate
from .dbschema import database_schema, UploadSchema
from .BioFile import genbank_parser
from .processing_utility import fix_multiple_splicing_bugs, ModelGFFDict, AnnotationData
from .taxomony import Taxonomy, DotsOrganism
from .dbtable_utility import TableStatusID, UploadTableData
from .process_tables import TableProcessUtility
from .protein_annotation_utility import ProteinAnnotations
from . import general_utility
_logger = logging.getLogger("galEupy.app")


class BaseApp(DatabaseConfig):
    def __init__(self, db_config_file):
        DatabaseConfig.__init__(self, db_config_file)
        """
        Basic entry options.
        db_config_file : Path
            database configuration file path
        """
        self.db_config_file = db_config_file

    @property
    def db_status(self):
        """
        checks database connection
        """
        db_status = check_db_connection(self.host, self.db_username, self.db_password, port=self.db_port)

        if db_status:
            _logger.debug("The database connection is fine")

            return True
        else:
            _logger.debug("There is an issue with the database connection")
            return False

    def db_schema(self):
        schema = UploadSchema(self.db_config_file)
        schema_existence = schema.check_schema_existence()

        if schema_existence:
            _logger.debug('Database Schemas are already exist')
            return True
        else:
            _logger.debug('Database Schemas are missing')
            return False

    def db_table_log(self):

        # db_name = DbNames(self.db_prefix)
        db_conn = Database(self.host, self.db_username, self.db_password, self.db_name, 1, port=self.db_port)
        table_stat = TableStatusID(db_conn)
        table_stat.show_id_log()
        table_stat.get_protein_feature_table_status()

    def drop_databases(self):
        query_response = query_yes_no("Would you like to delete the database")
        if query_response:
            db_obj = DatabaseCreate(self.host, self.db_username, self.db_password, port=self.db_port)
            if db_obj.db_existence(self.db_name) is not None:
                db_obj.drop_database(self.db_name)
            else:
                _logger.debug(f"Database {self.db_name} doesn't exist")

        else:
            _logger.debug("Database drop option skipped")


class OrganismApp(BaseApp, OrganismConf):
    def __init__(self, db_config_file, org_config_file):
        BaseApp.__init__(self, db_config_file)
        OrganismConf.__init__(self, org_config_file)

    def remove_organism_record(self):
        # db_name = DbNames(self.db_prefix)
        db_conn = Database(self.host, self.db_username, self.db_password, self.db_name, 1, port=self.db_port)
        organism_obj = DotsOrganism(db_conn, self.organism, self.version)
        organism_obj.remove_organism_record()

    def get_organism_record(self):
        # db_name = DbNames(self.db_prefix)
        db_conn = Database(self.host, self.db_username, self.db_password, self.db_name, 1, port=self.db_port)
        organism_obj = DotsOrganism(db_conn, self.organism, self.version)
        organism_obj.get_organism_record()


class App(ConfigFileHandler):
    def __init__(self, db_config_file, path_config_file, org_config_file):
        """ class constructor reads three configuration files
        parameters
        ---------
        db_config_file: string
            path for database configuration file
        path_config_file: basestring
            path for path related configuration file
        org_config_file: basestring
            path for organism configuration file

        """
        ConfigFileHandler.__init__(self, db_config_file, path_config_file, org_config_file)

    @property
    def check_db_status(self):
        _logger.debug("Check db connection: start")
        db_status = check_db_connection(self.db_config.host, self.db_config.db_username, self.db_config.db_password,
                                        port=self.db_config.db_port)
        _logger.debug("Check db connection: Complete")
        return db_status

    def upload_schema(self):
        if self.check_db_status:
            _logger.debug("Uploading Schema: start")
            database_schema(self.db_config_file)
            _logger.debug("Uploading Schema: Complete")
        else:
            _logger.info("Database schema already exists")

    def process_central_dogma_annotation(self):
        _logger.debug("Process central dogma data: start")

        app1 = CentralDogmaAnnotator(self.db_config, self.path_config, self.org_config)
        _logger.debug(f"Annotation type: {app1.annotation_type}")

        if app1.taxonomy_id_sres is None:
            _logger.error(f"""There is no entry with entered organism name: Please check the organism name
            Entered organism name: {app1.org_config.organism}""")
            app1.taxon_entries()

        elif app1.organism_existence is False:
            _logger.debug(f"Detected Datatype: {app1.annotation_type}")
            if app1.annotation_type == 'GenBank_Annotation':
                app1.process_genbank_annotation()
                app1.update_organism_table()

            if app1.annotation_type == 'Partial_Annotation':
                app1.process_partial_annotations()
                app1.update_organism_table()
                # app1.import_protein_annotation()

            if app1.annotation_type == 'Minimal_Annotation':
                app1.process_partial_annotations()
                app1.update_organism_table()

            if app1.annotation_type == 'No_Annotation':
                _logger.error("Under development")

    def import_protein_annotation(self):
        _logger.debug("Processing protein annotation data: start")
        random_string = general_utility.random_string(20)
        app1 = CentralDogmaAnnotator(self.db_config, self.path_config, self.org_config)

        if app1.taxonomy_id_sres is None:
            _logger.error(f"""There is no entry with entered organism name: Please check the organism name
            Entered organism name: {app1.org_config.organism}""")

        elif app1.organism_existence:
            taxonomy_id = app1.taxonomy_id_sres
            org_version = app1.org_config.version
            _logger.info("Preparing the protein annotation data")
            protein_annotation_obj = ProteinAnnotations(app1.db_dots, app1.path_config, app1.org_config, random_string,
                                                        taxonomy_id, org_version)
            # protein_annotation_obj.create_protein_file(app1.taxonomy_id_sres, app1.org_config.version)

            # upload InterProScan data
            if app1.org_config.interproscan:
                _logger.info("IntroProScan data is provided")
                if app1.org_config.interproscan.exists():
                    _logger.info("Processing IntroProScan data")
                    protein_annotation_obj.parse_interproscan_data(app1.org_config.interproscan)
                else:
                    _logger.error(f"Please check the path for InterProScan data\n Path: {app1.org_config.interproscan}")
            else:
                _logger.info("IntroProScan data is not provided")

            # for SignalP
            if app1.org_config.signalp:
                _logger.info("SignalP data is provided")
                if app1.org_config.signalp.exists():
                    _logger.info("Processing SignalP data")
                    protein_annotation_obj.parse_signalp_result(app1.org_config.signalp)
                    protein_annotation_obj.upload_signalp_data()
            else:
                _logger.info("SignalP data is not provided")

            # for tmhmm
            if app1.org_config.tmhmm:
                _logger.info("tmhmm data is provided")
                if app1.org_config.tmhmm.exists():
                    _logger.info("Processing tmhmm data")
                    protein_annotation_obj.parse_tmhmm_result(app1.org_config.tmhmm)
                    protein_annotation_obj.upload_tmhmm_data()
            else:
                _logger.info("tmhmm data is not provided")

            # Eggnog
            if app1.org_config.eggnog:
                _logger.info(f"eggnog data is provided: {app1.org_config.eggnog}")
                if app1.org_config.eggnog.exists():
                    _logger.info("Processing eggnog data")
                    protein_annotation_obj.parse_eggnog_result(app1.org_config.eggnog)
                    protein_annotation_obj.upload_eggnog_data()
            else:
                _logger.info("eggnog data is not provided")

    def db_table_logs(self):
        app1 = CentralDogmaAnnotator(self.db_config, self.path_config, self.org_config)
        app1.show_id_log()
        app1.get_protein_feature_table_status()


class AnnotationCategory:
    annotation_type_list = ["GenBank_Annotation", "No_Annotation", "Minimal_Annotation", "Partial_Annotation"]
    annotation_type_1 = annotation_type_list[0]
    annotation_type_2 = annotation_type_list[1]
    annotation_type_3 = annotation_type_list[2]
    annotation_type_4 = annotation_type_list[3]

    def __init__(self, org_config, path_config):
        """ class constructor for Annotation Category
        parameters
        ---------
        org_config: basestring
            path for organism configuration file
        path_config: basestring
            path for path related configuration file
        """
        self.org_config = org_config
        self.path_config = path_config

    @property
    def is_genbank(self):
        if self.org_config.GenBank is not None and self.org_config.GenBank != '':
            return True
        else:
            return False

    @property
    def annotation_type(self):
        """ return the annotation type"""

        if self.is_genbank:
            return self.annotation_type_1
        else:
            if self.org_config.fasta != "" and self.org_config.gff == "" and self.org_config.product == "":
                if self.org_config.ref_org != "" and self.org_config.upload_dir != "":
                    return self.annotation_type_2
                elif self.org_config == "":
                    _logger.info("Error: Reference Genome File does not exist")
                elif self.path_config.upload_dir == "":
                    _logger.info("Error: Upload path is empty")
            elif self.org_config.fasta != "" and self.org_config.gff != "" and self.org_config.product == "":
                return self.annotation_type_3
            elif self.org_config.fasta != "" and self.org_config.gff != "" and self.org_config.product != "":
                return self.annotation_type_4
            else:
                return None


class CentralDogmaAnnotator(AnnotationCategory, Taxonomy, TableStatusID):
    def __init__(self, db_config, path_config, org_config):
        AnnotationCategory.__init__(self, org_config, path_config)

        self.db_config = db_config
        self.org_config = org_config
        self.path_config = path_config

        self.db_connection = Database(db_config.host, db_config.db_username, db_config.db_password, db_config.db_name,
                                      1, port=db_config.db_port)

        self.file_upload = UploadTableData(self.db_connection, self.path_config.upload_dir)
        Taxonomy.__init__(self, self.db_connection, org_config.organism, org_config.version)
        TableStatusID.__init__(self, self.db_connection)

    def process_genbank_annotation(self):
        _logger.info('Processing  GenBank type Data: start')
        file_path = Path(self.org_config.GenBank)
        if not file_path.exists():
            file_path = self.org_config.config_file_path.parent.joinpath(file_path)

        if file_path.exists():
            file_handler = genbank_parser.open_input_file(file_path)
            (feature_dct, sequence_dct) = genbank_parser.get_data(file_handler)

            feature_dct = fix_multiple_splicing_bugs(feature_dct)
            model_gff_obj = ModelGFFDict(sequence_dct, feature_dct)
            model_gff_dct = model_gff_obj.create_model_dct()

            # (sequence_dct, feature_dct) = process_type1_data(org_config)
            self.minimal_annotation_data(sequence_dct, feature_dct)
            self.file_upload.upload_central_dogma_data()

        else:
            _logger.error("File not found: {}".format(self.org_config.GenBank))

    def process_partial_annotations(self):
        random_string = general_utility.random_string(20)

        annotation_obj = AnnotationData(self.org_config)
        feature_dct = annotation_obj.prepare_gal_model()

        self.minimal_annotation_data(annotation_obj.sequence_dct, feature_dct)
        self.file_upload.upload_central_dogma_data()

    def minimal_annotation_data(self, sequence_dct, feature_dct):

        taxonomy_id = self.taxonomy_id_sres
        _logger.info(f"Taxonomy_id: {taxonomy_id}")

        gal_table = TableProcessUtility(self.db_connection, self.path_config.upload_dir, self.org_config.organism,
                                        taxonomy_id, self.org_config.version)
        gal_table.show_id_log()
        gal_table.increase_by_value(1)

        for scaffold, scaffold_dct in feature_dct.items():
            if scaffold in sequence_dct:
                sequence = sequence_dct[scaffold]
                gal_table.na_sequenceimp_scaffold(gal_table.NaSequenceId, scaffold, sequence)
                scaffold_na_sequence_id = gal_table.NaSequenceId
                gal_table.NaSequenceId += 1
                for feature, feature_dct in scaffold_dct.items():
                    if feature == 'gene':
                        for gene_id, gene_dct in feature_dct.items():
                            gal_table.process_gff_gene_data(scaffold, gene_id, gene_dct, scaffold_na_sequence_id)
                            gal_table.NaSequenceId += 1
                    elif feature == 'repeat_region':
                        gal_table.process_repeat_data(feature, feature_dct, scaffold_na_sequence_id)

    def import_protein_annotation(self):
        _logger.debug("Processing protein annotation data: start")
        random_string = general_utility.random_string(20)

        if self.organism_existence:
            taxonomy_id = self.taxonomy_id_sres
            org_version = self.org_config.version
            _logger.info("Preparing the protein annotation data")
            protein_annotation_obj = ProteinAnnotations(self.db_connection, self.path_config, self.org_config,
                                                        random_string, taxonomy_id, org_version)
            # upload InterProScan data
            if self.org_config.interproscan:
                _logger.info("InterProScan data is provided")
                if self.org_config.interproscan.exists():
                    _logger.info("Processing InterProScan data")
                    protein_annotation_obj.parse_interproscan_data(self.org_config.interproscan)
                else:
                    _logger.error(f"Please check the path for InterProScan data\n Path: {self.org_config.interproscan}")
            else:
                _logger.info("IntroProScan data is not provided")

            # for SignalP
            if self.org_config.signalp:
                _logger.info("SignalP data is provided")
                if self.org_config.signalp.exists():
                    _logger.info("Processing SignalP data")
                    protein_annotation_obj.parse_signalp_result(self.org_config.signalp)
                    protein_annotation_obj.upload_signalp_data()
            else:
                _logger.info("SignalP data is not provided")

            if self.org_config.tmhmm:
                _logger.info("tmhmm data is provided")
                if self.org_config.tmhmm.exists():
                    _logger.info("Processing tmhmm data")
                    protein_annotation_obj.parse_tmhmm_result(self.org_config.tmhmm)
                    protein_annotation_obj.upload_tmhmm_data()
            else:
                _logger.info("tmhmm data is not provided")

            if self.org_config.eggnog:
                _logger.info(f"eggnog data is provided: {self.org_config.eggnog}")
            else:
                _logger.info("eggnog data is not provided")

            # show log
            protein_annotation_obj.show_id_log()
            protein_annotation_obj.get_protein_feature_table_status()


def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")