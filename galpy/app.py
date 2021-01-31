import logging
from pathlib import Path
from .configutility import ConfigFileHandler
from .dbconnect import check_db_connection, DbNames, Database
from .dbschema import database_schema
from .BioFile import genbank_parser
from .processingutility import fix_multiple_splicing_bugs, create_gal_model_dct
from .taxomony import Taxonomy, OrganismInfo
from .generalutility import get_date
from .dbtableutility import get_table_status, na_sequence_imp_scaffold, upload_gal_table_data
from .directoryutility import GALFileHandler
from .process_tables import process_gff_gene_data, process_repeat_data
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
        app1.process_genbank_annotation()


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
        db_name = DbNames(db_config.db_prefix)
        self.db_dots = Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)
        self.db_sres = Database(db_config.host, db_config.db_username, db_config.db_password, db_name.sres, 0)

    def process_genbank_annotation(self):
        _logger.info('Processing  GenBank type Data...')
        file_path = Path(self.org_config.GenBank)
        if not file_path.exists():
            file_path = self.org_config.config_file_path.parent.joinpath(file_path)

        if file_path.exists():
            file_handler = genbank_parser.open_input_file(file_path)
            (feature_dct, sequence_dct) = genbank_parser.get_data(file_handler)

            feature_dct = fix_multiple_splicing_bugs(feature_dct)
            model_gff_dct = create_gal_model_dct(sequence_dct, feature_dct)

            id_list = get_table_status(self.db_dots)
            # (sequence_dct, feature_dct) = process_type1_data(org_config)
            self.minimal_annotation_data(sequence_dct, feature_dct, id_list)
            upload_gal_table_data(self.db_config, self.path_config.upload_dir)
        else:
            _logger.error("File not found: {}".format(self.org_config.GenBank))

    def minimal_annotation_data(self, sequence_dct, feature_dct, id_list):
        taxonomy_1 = Taxonomy(self.org_config.organism, self.org_config.version)
        taxonomy_id = taxonomy_1.get_taxonomy_id(self.db_sres)
        _logger.info("taxonomy_id: {}".format(taxonomy_id))
        # taxonomy_id = organism_function.get_taxonomy_id(db_config, org_config.organism)
        org_info = OrganismInfo(self.org_config.organism, taxonomy_id, self.org_config.version)
        gal_id = DatabaseID(id_list)
        gal_fh = GALFileHandler(self.path_config.upload_dir)
        gal_id.increase_by_value(1)
        present_day = get_date()

        for scaffold, scaffold_dct in feature_dct.items():
            if scaffold in sequence_dct:
                sequence = sequence_dct[scaffold]
                na_sequence_imp_scaffold(gal_fh, gal_id.NaSequenceId, scaffold, sequence, org_info, present_day)
                scaffold_na_sequence_id = gal_id.NaSequenceId
                gal_id.NaSequenceId += 1
                for feature, feature_dct in scaffold_dct.items():
                    if feature == 'gene':
                        for gene_id, gene_dct in feature_dct.items():
                            process_gff_gene_data(gal_id, gal_fh, org_info, scaffold, gene_id, gene_dct,
                                                      scaffold_na_sequence_id)
                            gal_id.NaSequenceId += 1
                    elif feature == 'repeat_region':
                        process_repeat_data(gal_id, gal_fh, feature, feature_dct, scaffold_na_sequence_id)


class DatabaseID:
    def __init__(self, id_list):
        self.NaSequenceId = id_list[0]
        self.NaFeatureId = id_list[1]
        self.na_location_Id = id_list[2]
        self.GeneInstanceId = id_list[3]
        self.ProteinId = id_list[4]

    def increase_by_value(self, value):
        self.NaSequenceId += value
        self.NaFeatureId += value
        self.na_location_Id += value
        self.GeneInstanceId += value
        self.ProteinId += value