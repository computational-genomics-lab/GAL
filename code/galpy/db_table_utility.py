from __future__ import print_function
import re
from galpy import db_function, directory_utility, logging_utility

# import db_function
# import gal_function as galf


def get_sam_alignment_last_row_id(db_config):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)
    sql_1 = "SELECT MAX(SAM_ALIGNMENT_ID) AS LAST_ID FROM SamAlignment"
    row_sam_alignment = get_max_table_value(db_dots, sql_1)
    return row_sam_alignment


def get_table_status(db_config, log_filename):
    logger = logging_utility.logger_function(__name__, log_filename)
    # logger.info("\n\t\tGetting Max IDs of each table...............")

    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)

    sql_1 = "SELECT MAX(NA_SEQUENCE_ID) as LAST_ID FROM NASequenceImp"
    sql_2 = "SELECT MAX(NA_FEATURE_ID) as LAST_ID FROM NAFeatureImp"
    sql_3 = "SELECT MAX(NA_LOCATION_ID) as LAST_ID FROM NALocation"
    sql_4 = "SELECT MAX(GENE_INSTANCE_ID) as LAST_ID FROM GeneInstance"
    sql_5 = "SELECT MAX(PROTEIN_ID) as LAST_ID FROM Protein"

    row_na_sequence = get_max_table_value(db_dots, sql_1)
    row_na_feature = get_max_table_value(db_dots, sql_2)
    row_na_location = get_max_table_value(db_dots, sql_3)
    row_gene_instance = get_max_table_value(db_dots, sql_4)
    row_protein = get_max_table_value(db_dots, sql_5)

    print_str = """Getting Max IDs of each table..
        NASequenceImp ID: {}
        NAFeatureImp ID: {}
        NALocation ID: {}
        GeneInstance ID: {}
        Protein ID: {}
        """.format(row_na_sequence, row_na_feature, row_na_location, row_gene_instance, row_protein)

    logger.info(print_str)
    # print("\t\t  NASequenceImp ID is: %d " % row_na_sequence)
    # print("\t\t  NAFeatureimp ID is: %d " % row_na_feature)
    # print("\t\t  NALocation ID is: %d " % row_na_location)
    # print("\t\t  GeneInstance ID is: %d " % row_gene_instance)
    # print("\t\t  Protein ID is: %d " % row_protein)

    row_list = [row_na_sequence, row_na_feature, row_na_feature, row_na_feature, row_na_feature]
    return row_list


def get_protein_feature_table_status(db_config):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)

    sql_1 = "SELECT MAX(PFAM_ID) as LAST_ID FROM HmmPfam"
    sql_2 = "SELECT MAX(TMHMM_ID) as LAST_ID FROM Tmhmm"
    sql_3 = "SELECT MAX(SIGNALP_ID) as LAST_ID FROM SignalP"

    row_hmm_pfam = get_max_table_value(db_dots, sql_1)
    row_tmhmm = get_max_table_value(db_dots, sql_2)
    row_signalp = get_max_table_value(db_dots, sql_3)
    row_list = [row_hmm_pfam, row_tmhmm, row_signalp]
    return row_list


def get_interpro_scan_last_row_id(db_config):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)
    sql_1 = "SELECT MAX(interpro_scan_ID) AS LAST_ID FROM InterProScan"
    row_protein_instance_feature = get_max_table_value(db_dots, sql_1)
    return row_protein_instance_feature


def get_max_table_value(db, query):
    data = db.query_one(query)
    count = data['LAST_ID']
    if count is None:
        max_id = 0
    else:
        max_id = count
    return max_id


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


def get_sequence_string(sequence):
    base = BaseCount(sequence)
    length = base.length()
    base_count = base.print_base_count()
    sequence_string = '{}\t{}\t{}'.format(sequence, length, base_count)
    return sequence_string


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




def upload_gal_table_data(db_config, upload_dir, logger):

    db_name = db_function.DbNames(db_config.db_prefix)
    file_names = directory_utility.GalFileName(upload_dir)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 1)

    # For NASequenceImp table
    sql_1 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE NASequenceImp FIELDS TERMINATED BY '\t' OPTIONALLY
    ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.NaSequenceImp
    logger.debug(sql_1)
    db_dots.insert(sql_1)

    # For NAFeatureImp table
    sql_2 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE NAFeatureImp FIELDS TERMINATED BY '\t' 
    OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.NaFeatureImp
    logger.debug(sql_2)
    db_dots.insert(sql_2)

    # For NALocation table
    sql_3 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE NALocation FIELDS TERMINATED BY '\t' 
    OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.NaLocation
    logger.debug(sql_3)
    db_dots.insert(sql_3)

    # For GeneInstance table
    sql_4 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE GeneInstance FIELDS TERMINATED BY '\t' OPTIONALLY
    ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.GeneInstance
    logger.debug(sql_4)
    db_dots.insert(sql_4)

    # For Protein Table
    sql_5 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE Protein FIELDS TERMINATED BY '\t' OPTIONALLY
     ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % file_names.Protein
    logger.debug(sql_5)
    db_dots.insert(sql_5)


def upload_protein_feature_table_data(db_config, upload_dir_names):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 1)

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
