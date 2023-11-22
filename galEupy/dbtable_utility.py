import logging
from .directory_utility import UploadDirectory, GALFileHandler
from .general_utility import BaseCount
from .taxomony import OrganismName
from .general_utility import get_date
_logger = logging.getLogger("galEupy.dbtable_utility")


class TableStatusID:
    def __init__(self, db_dots):
        """ class constructor creates fetches the max values important tables

        parameters
        ---------
        db_dots: db connection for db_dots database
        """
        self.db_dots = db_dots

        sql_1 = "SELECT MAX(NA_SEQUENCE_ID) as LAST_ID FROM nasequenceimp"
        sql_2 = "SELECT MAX(NA_FEATURE_ID) as LAST_ID FROM nafeatureimp"
        sql_3 = "SELECT MAX(NA_LOCATION_ID) as LAST_ID FROM nalocation"
        sql_4 = "SELECT MAX(GENE_INSTANCE_ID) as LAST_ID FROM geneinstance"
        sql_5 = "SELECT MAX(PROTEIN_ID) as LAST_ID FROM protein"

        self.NaSequenceId = self.get_max_table_value(sql_1)
        self.NaFeatureId = self.get_max_table_value(sql_2)
        self.na_location_Id = self.get_max_table_value(sql_3)
        self.GeneInstanceId = self.get_max_table_value(sql_4)
        self.ProteinId = self.get_max_table_value(sql_5)

    def show_id_log(self):
        log_str = f"""Getting Max IDs of each table..
                        nasequenceimp ID: {self.NaSequenceId}
                        nafeatureimp ID: {self.NaFeatureId}
                        nalocation ID: {self.na_location_Id}
                        geneinstance ID: {self.GeneInstanceId}
                        protein ID: {self.ProteinId}"""
        _logger.info(log_str)

    def get_max_table_value(self, query):
        data = self.db_dots.query_one(query)
        count = data['LAST_ID']
        if count is None:
            max_id = 0
        else:
            max_id = count
        return max_id

    def increase_by_value(self, value):
        """
        It increases the value for each id by the value
        parameters
        ----------
        value: int
        """
        self.NaSequenceId += value
        self.NaFeatureId += value
        self.na_location_Id += value
        self.GeneInstanceId += value
        self.ProteinId += value

    def get_protein_feature_table_status(self):

        sql_1 = "SELECT MAX(pfam_ID) as LAST_ID FROM hmmpfam"
        sql_2 = "SELECT MAX(tmhmm_ID) as LAST_ID FROM tmhmm"
        sql_3 = "SELECT MAX(signalp_ID) as LAST_ID FROM signalp"
        sql_4 = "SELECT MAX(interpro_scan_ID) AS LAST_ID FROM interproscan"

        row_hmm_pfam = self.get_max_table_value(sql_1)
        row_tmhmm = self.get_max_table_value(sql_2)
        row_signalp = self.get_max_table_value(sql_3)
        row_protein_instance_feature = self.get_max_table_value(sql_4)

        row_dct = {
            'pfam': row_hmm_pfam,
            'tmhmm': row_tmhmm,
            'signalp': row_signalp,
            'interproscan': row_protein_instance_feature
        }

        log_str = f"""Getting Max IDs of each Protein Annotation table..
                        hmmpfam ID: {row_hmm_pfam}
                        signalp ID: {row_signalp}
                        tmhmm ID: {row_tmhmm}
                        interproscan ID: {row_protein_instance_feature}"""
        _logger.info(log_str)

        return row_dct


class DefaultVariables:
    externalDatabaseID = 8
    source_na_sequence_ID = 0
    sequence_piece_ID = 0
    sequencing_center_contact_ID = 1

    sequence_ontology_ID = 0
    external_database_ID = 7
    source_ID = 0
    prediction_algorithm_ID = 0
    review_status_ID = 3
    reviewer_summary = "Not Reviewed"
    is_predicted = 1
    gene_category_id = 1
    gene_instance_category_id = 1
    protein_instance_category_id = 1
    aa_feature_id = 1

    intA = '{}\t{}\t{}\t{}\t{}\t{}'.format("0", "0", "0", "0", "0", "0")

    def __init__(self):
        pass

    def data_source_id(self):
        return '{}\t{}\t{}\t{}'.format(self.externalDatabaseID, self.source_na_sequence_ID, self.sequence_piece_ID,
                                       self.sequencing_center_contact_ID)


class TableUtility(TableStatusID, OrganismName, DefaultVariables, GALFileHandler):
    def __init__(self, db_dots, upload_dir, organism, taxonomy_id, version):
        """ class constructor process the data for GAL table structure
        parameter
        ---------
        db_dots: db connection object
            db_dots database connection
        upload_dir: string - path
            path for creating temporary file
        organism: string
            organism name
        taxonomy_id: int
            taxonomy id for the organism
        version: str
            assembly version for the organism (i.e; 1, 2)

        """
        OrganismName.__init__(self, organism, version)
        self.taxonomy_id = taxonomy_id
        TableStatusID.__init__(self, db_dots)
        GALFileHandler.__init__(self, upload_dir)
        DefaultVariables.__init__(self)
        self.present_day = get_date()

    def na_sequenceimp_scaffold(self, na_sequence_id, scaffold, sequence):
        """
        creates a row in nasequenceimp table for a scaffold
        parameters
        --------
        na_sequence_id: int
            unique key for the scaffold
        scaffold: string
            scaffold name
        sequence: basestring
            sequence for the scaffold
        """
        subclass_view = "ExternalNASequence"
        sequence_type_id = 1
        gi_number = "GI:{}".format(scaffold)

        sequence_string = get_sequence_string(sequence)
        string1 = '{}\t{}\t{}\t{}\t{}\t{}'.format(na_sequence_id, self.org_version, subclass_view, sequence_type_id,
                                                  self.taxonomy_id, sequence_string)

        string2 = '{}\t{}\t{}\t{}'.format(self.org_name, 'NULL', self.sequence_piece_ID,
                                          self.sequencing_center_contact_ID)
        string3 = '{}\t{}\t{}\t{}'.format(self.present_day, scaffold, gi_number, scaffold)
        final_string = '{}\t{}\t{}\n'.format(string1, string2, string3)

        self.NaSequenceImp_fh.write(final_string)  # write to file
        return final_string

    def na_sequenceimp_gene(self, na_sequence_id, scaffold, source_na_sequence_id, gene_data):
        subclass_view = "ExternalNASequence"
        sequence_type_id = 6
        sequence_string = get_sequence_string(gene_data.gene_sequence)

        gi_number = "GI:{}".format(scaffold)
        description = "Unknown"

        string1 = '{}\t{}\t{}\t{}\t{}\t{}'.format(na_sequence_id, self.org_version, subclass_view, sequence_type_id,
                                                  self.taxonomy_id, sequence_string)
        string2 = '{}\t{}\t{}\t{}'.format(description, source_na_sequence_id, self.sequence_piece_ID,
                                          self.sequencing_center_contact_ID)
        string3 = '{}\t{}\t{}\t{}'.format(self.present_day, scaffold, gi_number, gene_data.gene_name)

        final_string = '{}\t{}\t{}\n'.format(string1, string2, string3)
        self.NaSequenceImp_fh.write(final_string)  # write to file
        return final_string

    def na_featureimp(self, na_feature_id, na_sequence_id, feature_type, name, parent_id):
        if name == 'gene':
            sub_class_view = 'gene'
        else:
            sub_class_view = feature_type
        external_database_id = 0
        source_id = 0
        prediction_algorithm_id = 0
        is_predicted = 0
        review_status_id = 0

        string1 = '{}\t{}\t{}\t{}\t{}'.format(na_feature_id, na_sequence_id, sub_class_view, feature_type, name)

        string2 = '{}\t{}\t{}\t{}\t{}\t{}'.format(parent_id, external_database_id, source_id, prediction_algorithm_id,
                                                  is_predicted, review_status_id)

        final_string = '{}\t{}\n'.format(string1, string2)
        self.NaFeatureImp_fh.write(final_string)
        return final_string

    def na_featureimp_rna(self, na_feature_id, na_sequence_id, feature_type, name, parent_id):
        sub_class_view = feature_type

        external_database_id = 0
        source_id = 0
        prediction_algorithm_id = 0
        is_predicted = 0
        review_status_id = 0

        string1 = '{}\t{}\t{}\t{}\t{}'.format(na_feature_id, na_sequence_id, sub_class_view, feature_type, name)

        string2 = '{}\t{}\t{}\t{}\t{}\t{}'.format(parent_id, external_database_id, source_id, prediction_algorithm_id,
                                                  is_predicted, review_status_id)
        final_string = '{}\t{}\n'.format(string1, string2)
        self.NaFeatureImp_fh.write(final_string)
        return final_string

    def na_location(self, na_location_id, na_feature_id, start_location, end_location, is_reversed):
        loc_order = 0
        is_excluded = 3
        literal_sequence = ''
        location_type = ''

        string1 = '{}\t{}\t{}\t{}\t{}\t{}'.format(na_location_id, na_feature_id, start_location, start_location,
                                                  end_location, end_location)
        string2 = '{}\t{}\t{}\t{}\t{}'.format(loc_order, is_reversed, is_excluded, literal_sequence, location_type)

        final_string = '{}\t{}\n'.format(string1, string2)
        self.NALocation_fh.write(final_string)
        return final_string

    def gene_instance(self, gene_instance_id, na_feature_id, annotation):
        review_summary = None
        is_reference = 0
        review_status_id = 0
        string1 = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(gene_instance_id, na_feature_id, annotation, review_summary,
                                                        is_reference, review_status_id, self.present_day)
        self.GeneInstance_fh.write(string1)
        return string1

    def protein(self, protein_id, name, description, gene_instance_id, protein_sequence):
        review_status_id = 0
        review_summary = None
        string1 = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(protein_id, name, description, review_status_id, review_summary,
                                                        gene_instance_id, protein_sequence)
        self.Protein_fh.write(string1)
        return string1


def get_sequence_string(sequence):
    base = BaseCount(sequence)
    length = base.length()
    base_count = base.print_base_count()
    sequence_string = '{}\t{}\t{}'.format(sequence, length, base_count)
    return sequence_string


class UploadTableData(UploadDirectory):
    def __init__(self, db_connection, upload_dir):

        UploadDirectory.__init__(self, upload_dir)
        self.db = db_connection

    def upload_central_dogma_data(self):
        _logger.info("Uploading central dogma data: start")
        self.upload_na_sequenceimp()
        self.upload_na_featureimp()
        self.upload_nalocation()
        self.upload_geneinstance()
        self.protein()

    def upload_na_sequenceimp(self):
        # For NASequenceImp table
        columns = ['na_sequence_ID', 'sequence_version', 'subclass_view', 'sequence_type_ID', 'taxon_ID', 'sequence',
                   'length', 'a_count', 't_count', 'g_count', 'c_count', 'other_count', 'description',
                   'source_na_sequence_ID', 'sequence_piece_ID', 'sequencing_center_contact_ID', 'modification_date',
                   'string1', 'string2', 'string3']
        sql_1 = f"""LOAD DATA LOCAL INFILE '{self.NaSequenceImp}' 
        INTO TABLE nasequenceimp 
        FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"' 
        LINES TERMINATED BY '\n' 
        ({', '.join(columns)});"""

        _logger.debug(sql_1)
        self.db.insert(sql_1)

    def upload_na_featureimp(self):
        # For NAFeatureImp table
        columns = ["na_feature_ID", "na_sequence_ID", "subclass_view", "feature_type", "name", "parent_ID",
                   "external_database_id", "source_id", "prediction_algorithm_id", "is_predicted", "review_status_id"]

        # sql_2 = f"""LOAD DATA LOCAL INFILE '{self.NaFeatureImp}' INTO TABLE nafeatureimp FIELDS TERMINATED BY '\t'
        #            OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';"""

        sql_2 = f""" LOAD DATA LOCAL INFILE '{self.NaFeatureImp}'
        INTO TABLE nafeatureimp
        FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\n' ({', '.join(columns)});"""

        _logger.debug(sql_2)
        self.db.insert(sql_2)

    def upload_nalocation(self):
        # For NALocation table
        sql_3 = f"""LOAD DATA LOCAL INFILE '{self.NaLocation}' INTO TABLE nalocation FIELDS TERMINATED BY '\t' 
                    OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';"""
        _logger.debug(sql_3)
        self.db.insert(sql_3)

    def upload_geneinstance(self):
        sql_4 = f"""LOAD DATA LOCAL INFILE '{self.GeneInstance}' INTO TABLE geneinstance 
        FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n';"""
        _logger.debug(sql_4)
        self.db.insert(sql_4)

    def protein(self):
        # For Protein Table
        sql_5 = f"""LOAD DATA LOCAL INFILE '{self.Protein}' INTO TABLE protein FIELDS TERMINATED BY '\t' OPTIONALLY
                     ENCLOSED BY '"' LINES TERMINATED BY '\n';"""
        _logger.debug(sql_5)
        self.db.insert(sql_5)

    def protein_feature_data(self, upload_dir_names):
        pfam_upload_file = upload_dir_names.PFam
        signalp_upload_file = upload_dir_names.SignalP
        tmhmm_upload_file = upload_dir_names.TmHmm

        # For HmmPfam table
        sql_1 = f"""LOAD DATA LOCAL INFILE '{pfam_upload_file}' INTO TABLE hmmpfam FIELDS TERMINATED BY '\t' OPTIONALLY
           ENCLOSED BY '"' LINES TERMINATED BY '\n'
        (`pfam_ID`, `gene_instance_ID`, `e_value`, `score`, `bias`, `accession_id`, `domain_name`, `domain_description`)
        """
        self.db.insert(sql_1)

        # signalp table
        sql_2 = f"""LOAD DATA LOCAL INFILE '{signalp_upload_file}' INTO TABLE signalp 
        FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n'"""
        self.db.insert(sql_2)

        # For Tmhmm table
        sql_3 = f"""LOAD DATA LOCAL INFILE '{tmhmm_upload_file}' INTO TABLE tmhmm FIELDS TERMINATED BY '\t' OPTIONALLY
               ENCLOSED BY '"' LINES TERMINATED BY '\n'
               (`tmhmm_ID`, `gene_instance_ID`, `inside`, `outside`, `tmhelix`)"""
        self.db.insert(sql_3)
        _logger.info("Uploading central dogma data: complete")
