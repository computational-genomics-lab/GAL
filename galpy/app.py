import logging
from .configutility import ConfigFileHandler
from .dbconnect import check_db_connection
from .dbschema import database_schema
from .BioFile import genbank_parser
from .processingutility import fix_multiple_splicing_bugs, create_gal_model_dct
_logger = logging.getLogger("galpy.app")


class App(ConfigFileHandler):
    def __init__(self, db_config_file, path_config_file, org_config_file):
        ConfigFileHandler.__init__(self, db_config_file, path_config_file, org_config_file)

    @property
    def check_db_status(self):
        db_status = check_db_connection(self.db_config.host, self.db_config.db_username, self.db_config.db_password)
        return db_status

    def upload_schema(self):
        if self.check_db_status:
            database_schema(self.db_config)
        else:
            _logger.info("Database schema already exists")

    def process_central_dogma_annotation(self):
        app1 = CentralDogmaAnnotator(self.db_config, self.path_config, self.org_config)
        print(app1.annotation_type)


class AnnotationCategory:
    annotation_type_list = ["GenBank_Annotation", "No_Annotation", "Minimal_Annotation", "Partial_Annotation"]
    annotation_type_1 = annotation_type_list[0]
    annotation_type_2 = annotation_type_list[1]
    annotation_type_3 = annotation_type_list[2]
    annotation_type_4 = annotation_type_list[3]

    def __init__(self, org_config, path_config):
        self.org_config = org_config
        self.path_config = path_config

    @property
    def annotation_type(self):

        if self.org_config.GenBank != '':
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


class CentralDogmaAnnotator(AnnotationCategory):
    def __init__(self, db_config, path_config, org_config):
        AnnotationCategory.__init__(self, org_config, path_config)
        self.db_config = db_config
        self.org_config = org_config
        self.path_config = path_config

    def process_genbank_annotation(self):
        _logger.info('Processing  GenBank type Data...')
        file_handler = genbank_parser.open_input_file(self.org_config.GenBank)
        (feature_dct, sequence_dct) = genbank_parser.get_data(file_handler)

        feature_dct = fix_multiple_splicing_bugs(feature_dct)
        model_gff_dct = create_gal_model_dct(sequence_dct, feature_dct)

        # (sequence_dct, feature_dct) = process_type1_data(org_config)
        # process_minimal_annotation_data(db_config, org_config, path_config, sequence_dct, feature_dct, id_list)
        # db_table.upload_gal_table_data(db_config, path_config.upload_dir, logger)

