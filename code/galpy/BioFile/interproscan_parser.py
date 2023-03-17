import os
import re
from galeupy import db_function, db_table_utility


def process_interpro_data(db_config, upload_path, interpro_file, taxonomy_id, org_version):
    """
    This function parses a interproscan file data.
    """

    pif_id = db_table_utility.get_interpro_scan_last_row_id(db_config)
    parsed_file = get_interpro_parsed_file_name(upload_path)
    gene_name_dct = get_gene_name_map(db_config, taxonomy_id, org_version)
    parse_interpro(interpro_file, parsed_file, gene_name_dct, pif_id)

    upload_interpro_data(db_config, parsed_file)


def parse_interpro(interpro_file, parsed_file_name, gene_name_dct, pif_id):

    """This function parse a InterPro formatted file and return database format file """
    ipr_feature = "InterPro"
    go_feature = "GO"
    domain_name = ''

    parsed_fh = open(parsed_file_name, 'w')
    pif_id += 1
    read_fh = open(interpro_file, 'r')
    for i, line in enumerate(read_fh):
        if re.search(r'^@', line):
            continue
        if re.search(r'^#', line):
            continue
        tmp = re.split(r'\t', line)

        gene_name = tmp[0]
        if gene_name in gene_name_dct:
            protein_instance_id = gene_name_dct[gene_name]
        else:
            print('{} name is not matching with the database entry'.format(gene_name))
            continue
        start = int(tmp[6])
        stop = int(tmp[7])
        length = stop - start
        pval_mant = tmp[8]
        pval_exp = 0
        common_string = '{}\t{}\t{}\t1\t{}\t{}'.format(start, stop, length, pval_mant, pval_exp)

        if tmp[3] == 'ProSiteProfiles':
            feature_name = "ProfileScan"
        elif tmp[3] == 'SMART':
            feature_name = "HmmSmart"
        elif tmp[3] == 'PRINTS':
            feature_name = "FprintScan"
        else:
            continue

        if len(tmp) > 11:
            if len(tmp) >= 13:
                domain_name = tmp[12]
            if not re.match(r'^GO', tmp[13]) and re.match(r'^IPR', tmp[11]):
                    ipr = re.split(r'\|', tmp[11])
                    for ipr_value in ipr:
                        print_parsed_result(parsed_fh, pif_id, protein_instance_id, ipr_feature, common_string, domain_name, ipr_value, '')
                        pif_id += 1

            elif re.match(r'^IPR', tmp[11]) and re.match(r'^GO', tmp[13]):
                go = re.split(r'\|', tmp[13].rstrip('\n'))
                prediction_id = tmp[11]
                for go_value in go:
                    print_parsed_result(parsed_fh, pif_id, protein_instance_id, go_feature, common_string, domain_name, prediction_id, go_value)
                    pif_id += 1

        prediction_id = tmp[4]
        print_parsed_result(parsed_fh, pif_id, protein_instance_id, feature_name, common_string, domain_name, prediction_id, '')

        pif_id += 1


def print_parsed_result(parsed_fh, pif_id, protein_instance_id, feature_name, common_string, domain_name, prediction_id, go_id):
    bit_score = 1
    is_reviewed = 0
    string1 = '{}\t{}\t{}\t{}\t{}'.format(pif_id, protein_instance_id, feature_name, feature_name, common_string)
    string2 = '{}\t{}\t{}\t{}\t{}\t{}'.format(bit_score, domain_name, prediction_id, go_id, is_reviewed, 1)
    final_string = '{}\t{}\tNULL\n'.format(string1, string2)
    parsed_fh.write(final_string)
    return final_string


def upload_interpro_data(db_config, interpro_data):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 1)

    # For proteininstancefeature table
    sql_1 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE InterProScan FIELDS TERMINATED BY '\t' OPTIONALLY
        ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % interpro_data
    # print(sql_1)
    db_dots.insert(sql_1)


def get_gene_name_map(db_config, taxonomy_id, org_version):

    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)

    sql_query = """select p.name as 'name1',naf.name as 'name2', gi.gene_instance_id from 
Protein p, GeneInstance gi, NAFeatureImp naf, NASequenceImp na where 
gi.gene_instance_id = p.gene_instance_id and
naf.na_feature_id = gi.na_feature_id and
naf.feature_type='mRNA' and
na.na_sequence_id = naf.na_sequence_id and 
na.taxon_id = %s and
na.sequence_version = %s""" % (taxonomy_id, org_version)

    gene_name_dct = {}

    result = db_dots.query(sql_query)
    for i, value in enumerate(result):
        name1 = value['name1']
        name2 = value['name2']
        gene_instance_id = value['gene_instance_id']

        modified_gene_name = modify_gene_name(name1)
        gene_name_dct[modified_gene_name] = gene_instance_id
        gene_name_dct[name2] = gene_instance_id

    return gene_name_dct


def modify_gene_name(gene_name):
    modified_gene_name = ''
    match_obj = re.search(r'\S+_(\S+)', gene_name, re.M | re.I)
    if match_obj:
        modified_gene_name = match_obj.group(1)

    transcript_prefix = '.t1'
    modified_gene_name = '{}{}'.format(modified_gene_name, transcript_prefix)

    return modified_gene_name


def get_interpro_parsed_file_name(path):
    """It returns the parsed_sam_file path """
    filename = "parsed_interpro_file"
    parsed_file_name = os.path.join(path, filename)
    return parsed_file_name
