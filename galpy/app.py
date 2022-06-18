import logging
from pathlib import Path
from .configutility import ConfigFileHandler
from .dbconnect import check_db_connection, DbNames, Database
from .dbschema import database_schema
from .BioFile import genbank_parser
from .processingutility import fix_multiple_splicing_bugs, create_gal_model_dct
from .taxomony import Taxonomy, OrganismInfo
from .dbtableutility import TableStatusID, UploadTableData
from .process_tables import TableProcessUtility
_logger = logging.getLogger("galpy.app")


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
            database_schema(self.db_config)
            _logger.debug("Uploading Schema: Complete")
        else:
            _logger.info("Database schema already exists")

    def process_central_dogma_annotation(self):
        _logger.debug("Process central dogma data: start")
        app1 = CentralDogmaAnnotator(self.db_config, self.path_config, self.org_config)
        _logger.debug(f"annotation type: {app1.annotation_type}")
        if app1.organism_existence(app1.db_sres, app1.db_dots) is False:
            app1.process_genbank_annotation()
            app1.update_organism_table(app1.db_dots, app1.db_sres)
            # _logger.debug("Process central dogma data: start")
        else:
            _logger.debug("Table Max ids")
            TableStatusID(app1.db_dots, app1.path_config.upload_dir)


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
    def annotation_type(self):
        """ return the annotation type"""

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


class CentralDogmaAnnotator(AnnotationCategory, Taxonomy):
    def __init__(self, db_config, path_config, org_config):
        AnnotationCategory.__init__(self, org_config, path_config)
        Taxonomy.__init__(self, org_config.organism, org_config.version)
        self.db_config = db_config
        self.org_config = org_config
        self.path_config = path_config
        db_name = DbNames(db_config.db_prefix)
        self.db_dots = Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 1,
                                port=db_config.db_port)
        self.db_sres = Database(db_config.host, db_config.db_username, db_config.db_password, db_name.sres, 0,
                                port=db_config.db_port)
        self.file_upload = UploadTableData(self.db_dots, self.path_config.upload_dir)

    def process_genbank_annotation(self):
        _logger.info('Processing  GenBank type Data: start')
        file_path = Path(self.org_config.GenBank)
        if not file_path.exists():
            file_path = self.org_config.config_file_path.parent.joinpath(file_path)

        if file_path.exists():
            file_handler = genbank_parser.open_input_file(file_path)
            (feature_dct, sequence_dct) = genbank_parser.get_data(file_handler)

            feature_dct = fix_multiple_splicing_bugs(feature_dct)
            model_gff_dct = create_gal_model_dct(sequence_dct, feature_dct)

            # (sequence_dct, feature_dct) = process_type1_data(org_config)
            self.minimal_annotation_data(sequence_dct, feature_dct)
            self.file_upload.upload_central_dogma_data()

        else:
            _logger.error("File not found: {}".format(self.org_config.GenBank))

    def minimal_annotation_data(self, sequence_dct, feature_dct):
        taxonomy_1 = Taxonomy(self.org_config.organism, self.org_config.version)
        taxonomy_id = taxonomy_1.get_taxonomy_id(self.db_sres)
        _logger.info("taxonomy_id: {}".format(taxonomy_id))

        gal_table = TableProcessUtility(self.db_dots, self.path_config.upload_dir, self.org_config.organism,
                                        taxonomy_id, self.org_config.version)
        gal_table.increase_by_value(1)

        for scaffold, scaffold_dct in feature_dct.items():
            if scaffold in sequence_dct:
                sequence = sequence_dct[scaffold]
                gal_table.na_sequenceimp_scaffold( gal_table.NaSequenceId, scaffold, sequence)
                scaffold_na_sequence_id = gal_table.NaSequenceId
                gal_table.NaSequenceId += 1
                for feature, feature_dct in scaffold_dct.items():
                    if feature == 'gene':
                        for gene_id, gene_dct in feature_dct.items():
                            gal_table.process_gff_gene_data(scaffold, gene_id, gene_dct, scaffold_na_sequence_id)
                            gal_table.NaSequenceId += 1
                    elif feature == 'repeat_region':
                        gal_table.process_repeat_data(feature, feature_dct, scaffold_na_sequence_id)
