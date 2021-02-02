import logging
import re
from .dbconnect import DbNames, Database
from .directoryutility import UploadDirectory,GALFileHandler
from .generalutility import BaseCount
from .taxomony import OrganismInfo
from .generalutility import get_date
_logger = logging.getLogger("galpy.dbtableutility")


class TableStatusID(GALFileHandler):
    def __init__(self, db_dots, upload_dir):
        """ class constructor creates fetches the max values important tables
        parameters
        ---------
        db_dots: db connection for db_dots database
        """
        GALFileHandler.__init__(self, upload_dir)
        self.db_dots = db_dots

        sql_1 = "SELECT MAX(NA_SEQUENCE_ID) as LAST_ID FROM NASequenceImp"
        sql_2 = "SELECT MAX(NA_FEATURE_ID) as LAST_ID FROM NAFeatureImp"
        sql_3 = "SELECT MAX(NA_LOCATION_ID) as LAST_ID FROM NALocation"
        sql_4 = "SELECT MAX(GENE_INSTANCE_ID) as LAST_ID FROM GeneInstance"
        sql_5 = "SELECT MAX(PROTEIN_ID) as LAST_ID FROM Protein"

        self.NaSequenceId = self.get_max_table_value( sql_1)
        self.NaFeatureId = self.get_max_table_value(sql_2)
        self.na_location_Id = self.get_max_table_value(sql_3)
        self.GeneInstanceId = self.get_max_table_value(sql_4)
        self.ProteinId = self.get_max_table_value(sql_5)

        log_str = """Getting Max IDs of each table..
                NASequenceImp ID: {}
                NAFeatureImp ID: {}
                NALocation ID: {}
                GeneInstance ID: {}
                Protein ID: {}
                """.format(self.NaSequenceId, self.NaFeatureId, self.na_location_Id, self.GeneInstanceId, self.ProteinId)
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
        It increase the value for each id by the value
        parameters
        ----------
        value: int
        """
        self.NaSequenceId += value
        self.NaFeatureId += value
        self.na_location_Id += value
        self.GeneInstanceId += value
        self.ProteinId += value


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


class TableUtility(TableStatusID, OrganismInfo, DefaultVariables):
    def __init__(self, db_dots, upload_dir, organism, taxonomy_id, version):
        """ class constructor process the data for GAL table structure
        paramter
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
        OrganismInfo.__init__(self, organism, taxonomy_id, version)
        TableStatusID.__init__(self, db_dots, upload_dir)
        DefaultVariables.__init__(self)
        self.present_day = get_date()

    def na_sequenceimp_scaffold(self, na_sequence_id, scaffold, sequence):
        """
        creates a row in nasequenceimp table for a scaffold
        parameters
        --------
        na_sequence_id: int
            unique key for the sacffold
        scaffold: string
            scaffold name
        sequence: basestring
            sequence for the scaffold
        """
        subclass_view = "ExternalNASequence"
        sequence_type_id = 1
        gi_number = "GI:" + scaffold

        sequence_string = get_sequence_string(sequence)
        string1 = '{}\t{}\t{}\t{}\t{}\t{}'.format(na_sequence_id, self.version, subclass_view, sequence_type_id,
                                                  self.taxonomy_id, sequence_string)

        string2 = '{}\t{}\t{}\t{}'.format(self.organism, 'NULL', self.sequence_piece_ID,
                                          self.sequencing_center_contact_ID)
        string3 = '{}\t{}\t{}\t{}'.format(self.present_day, scaffold, gi_number, scaffold)
        final_string = '{}\t{}\t{}\n'.format(string1, string2, string3)

        self.NaSequenceImp_fh.write(final_string)  # write to file
        return final_string

    def na_sequenceimp_gene(self, na_sequence_id, source_na_sequence_id, scaffold, gene_data):
        subclass_view = "ExternalNASequence"
        sequence_type_id = 6
        sequence_string = get_sequence_string(gene_data.gene_sequence)
        gi_number = "GI:" + scaffold
        description = "Unknown"

        string1 = '{}\t{}\t{}\t{}\t{}\t{}'.format(na_sequence_id, self.version, subclass_view, sequence_type_id,
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


'''
def na_sequence_imp_scaffold(gal_fh, na_sequence_id, scaffold, sequence, org_info, present_day):
    subclass_view = "ExternalNASequence"
    # description = "unknown"
    sequence_type_id = 1

    organism = org_info.organism
    taxonomy_id = org_info.taxonomy_id
    version = org_info.version
    gi_number = "GI:" + scaffold

    default_variables = DefaultVariables()

    sequence_string = get_sequence_string(sequence)

    string1 = '{}\t{}\t{}\t{}\t{}\t{}'.format(na_sequence_id, version, subclass_view, sequence_type_id, taxonomy_id,
                                              sequence_string)
    string2 = '{}\t{}\t{}\t{}'.format(organism, 'NULL', default_variables.sequence_piece_ID,
                                      default_variables.sequencing_center_contact_ID)
    string3 = '{}\t{}\t{}\t{}'.format(present_day, scaffold, gi_number, scaffold)

    final_string = '{}\t{}\t{}\n'.format(string1, string2, string3)

    gal_fh.NaSequenceImp_fh.write(final_string)  # write to file
    return final_string


def na_sequence_imp_gene(gal_fh, na_sequence_id, org_info, scaffold, source_na_sequence_id, gene_data, present_day):

    subclass_view = "ExternalNASequence"
    sequence_type_id = 6
    default_variables = DefaultVariables()
    sequence_string = get_sequence_string(gene_data.gene_sequence)
    gi_number = "GI:" + scaffold
    description = "Unknown"

    organism = org_info.organism
    taxonomy_id = org_info.taxonomy_id
    org_version = org_info.version

    string1 = '{}\t{}\t{}\t{}\t{}\t{}'.format(na_sequence_id, org_version, subclass_view, sequence_type_id,
                                              taxonomy_id, sequence_string)
    string2 = '{}\t{}\t{}\t{}'.format(description, source_na_sequence_id, default_variables.sequence_piece_ID,
                                      default_variables.sequencing_center_contact_ID)
    string3 = '{}\t{}\t{}\t{}'.format(present_day, scaffold, gi_number, gene_data.gene_name)

    final_string = '{}\t{}\t{}\n'.format(string1, string2, string3)
    gal_fh.NaSequenceImp_fh.write(final_string)  # write to file
    return final_string


def na_feature_imp(gal_fh, na_feature_id, na_sequence_id, feature_type, name, parent_id):
    sub_class_view = ""
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
    gal_fh.NaFeatureImp_fh.write(final_string)
    return final_string


def na_feature_imp_rna(gal_fh, na_feature_id, na_sequence_id, feature_type, name, parent_id):
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
    gal_fh.NaFeatureImp_fh.write(final_string)
    return final_string


def na_location(gal_fh, na_location_id, na_feature_id, start_location, end_location, is_reversed):
    loc_order = 0
    is_excluded = 3
    literal_sequence = ''
    location_type = ''

    string1 = '{}\t{}\t{}\t{}\t{}\t{}'.format(na_location_id, na_feature_id, start_location, start_location,
                                              end_location, end_location)
    string2 = '{}\t{}\t{}\t{}\t{}'.format(loc_order, is_reversed, is_excluded, literal_sequence, location_type)

    final_string = '{}\t{}\n'.format(string1, string2)
    gal_fh.NALocation_fh.write(final_string)
    return final_string


def gene_instance(gal_fh, gene_instance_id, na_feature_id, annotation, present_day):
    review_summary = None
    is_reference = 0
    review_status_id = 0
    string1 = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(gene_instance_id, na_feature_id, annotation, review_summary,
                                                    is_reference, review_status_id, present_day)
    gal_fh.GeneInstance_fh.write(string1)
    return string1


def protein(gal_fh, protein_id, name, description, gene_instance_id, protein_sequence):
    review_status_id = 0
    review_summary = None
    string1 = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(protein_id, name, description, review_status_id, review_summary,
                                                    gene_instance_id, protein_sequence)
    gal_fh.Protein_fh.write(string1)
    return string1
'''




def get_sequence_string(sequence):
    base = BaseCount(sequence)
    length = base.length()
    base_count = base.print_base_count()
    sequence_string = '{}\t{}\t{}'.format(sequence, length, base_count)
    return sequence_string






def upload_gal_table_data(db_config, upload_dir):

    db_name = DbNames(db_config.db_prefix)
    file_names = UploadDirectory(upload_dir)
    db_dots = Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 1)

    # For NASequenceImp table
    sql_1 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE NASequenceImp FIELDS TERMINATED BY '\t' OPTIONALLY
    ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.NaSequenceImp
    _logger.debug(sql_1)
    db_dots.insert(sql_1)

    # For NAFeatureImp table
    sql_2 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE NAFeatureImp FIELDS TERMINATED BY '\t' 
    OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.NaFeatureImp
    _logger.debug(sql_2)
    db_dots.insert(sql_2)

    # For NALocation table
    sql_3 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE NALocation FIELDS TERMINATED BY '\t' 
    OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.NaLocation
    _logger.debug(sql_3)
    db_dots.insert(sql_3)

    # For GeneInstance table
    sql_4 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE GeneInstance FIELDS TERMINATED BY '\t' OPTIONALLY
    ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.GeneInstance
    _logger.debug(sql_4)
    db_dots.insert(sql_4)

    # For Protein Table
    sql_5 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE Protein FIELDS TERMINATED BY '\t' OPTIONALLY
     ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.Protein
    _logger.debug(sql_5)
    db_dots.insert(sql_5)


def upload_protein_feature_table_data(db_config, upload_dir_names):
    db_name = DbNames(db_config.db_prefix)
    db_dots = Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 1)

    pfam_upload_file = upload_dir_names.PFam
    signalp_upload_file = upload_dir_names.SignalP
    tmhmm_upload_file = upload_dir_names.TmHmm

    # For HmmPfam table
    sql_1 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE HmmPfam FIELDS TERMINATED BY '\t' OPTIONALLY
       ENCLOSED BY '"' LINES TERMINATED BY '\n'
       (`PFAM_ID`, `GENE_INSTANCE_ID`, `E_VALUE`, `SCORE`, `BIAS`, `ACCESSION_ID`, `DOMAIN_NAME`, `DOMAIN_DESCRIPTION`)
       """ % pfam_upload_file
    db_dots.insert(sql_1)

    # signalp table
    sql_2 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE SignalP FIELDS TERMINATED BY '\t' OPTIONALLY
           ENCLOSED BY '"' LINES TERMINATED BY '\n'""" % signalp_upload_file
    db_dots.insert(sql_2)

    # For Tmhmm table
    sql_3 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE Tmhmm FIELDS TERMINATED BY '\t' OPTIONALLY
           ENCLOSED BY '"' LINES TERMINATED BY '\n'
           (`TMHMM_ID`, `GENE_INSTANCE_ID`, `INSIDE`, `OUTSIDE`, `TMHELIX`)""" % tmhmm_upload_file
    db_dots.insert(sql_3)
