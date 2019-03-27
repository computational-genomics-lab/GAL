import os
import errno
import re
import collections
from collections import defaultdict
from galpy import db_function, external_program, logging_utility


def process_sam_alignment(db_config, path_config, sam_id, log_file):
    """This is the first need to call. This function does the following things
     1. call create_fasta_for_gal() function that creates the fasta files for the program
     2. call run_sam_alignment() function : ran lastz program
     3. call parse_sam() function : parse sam file
     4. call upload_sam_data() function : upload the parsed data into the database.
     """
    upload_path = path_config.upload_dir
    lastz_program = path_config.lastz
    logger = logging_utility.logger_function(__name__, log_file)
    sam_path = create_sam_alignment_directory(upload_path)
    sam_file_list = find_uploaded_sam_files(db_config, sam_path)
    organism_hierarchy_dct = get_organism_hierarchy_map(db_config)

    sequence_file_list = create_sequence_file_for_gal_using_dct(db_config, sam_path)
    sam_output_file_list = run_sam_alignment(lastz_program, organism_hierarchy_dct, sequence_file_list, sam_file_list,
                                             sam_path, log_file)

    if sam_output_file_list:
        parsed_sam_file = get_sam_parsed_file_name(sam_path)
        parsed_sam_fh = open(parsed_sam_file, 'w')

        for sam_output in sam_output_file_list:
            sam_file_path = os.path.join(sam_path, sam_output)
            sam_id = parse_sam(sam_file_path, sam_id, parsed_sam_fh)

        upload_sam_data(db_config, parsed_sam_file)


def create_sequence_file_for_gal_using_dct(db_config, path):
    """
    This function checks and creates fasta file for sam
    It returns the fasta file path associated with its taxonomy id and version
    """
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)

    sql_query = "SELECT * FROM NASequenceImp WHERE SEQUENCE_TYPE_ID =1 order by taxon_id, sequence_version"
    result = db_dots.query(sql_query)

    # collect data into a dict
    dct = defaultdict(lambda: defaultdict(lambda: defaultdict()))
    for i, value in enumerate(result):
        dct[value['TAXON_ID']][value['SEQUENCE_VERSION']][value['NA_SEQUENCE_ID']] = value['SEQUENCE']

    file_list = []
    # write the data into the file
    for taxonomy_id, version_dct in dct.items():
        for version, sequence_dct in version_dct.items():
            filename = "{}_{}.fasta".format(taxonomy_id, version)
            file_path = os.path.join(path, filename)
            file_list.append(filename)
            with open(file_path, 'w') as fh:
                for na_sequence_id, sequence in sequence_dct.items():
                    sequence_string = ">{}_{}_{}\n{}\n".format(na_sequence_id, taxonomy_id, version, sequence)
                    fh.write(sequence_string)
    return file_list


def run_sam_alignment(program, organism_hierarchy_dct, file_name_list, uploaded_sam_file_list, path, log_file):
    """
        This function RUNs the LastZ program and parse the SAM file.
    """
    logger = logging_utility.logger_function(__name__, log_file)
    class_level = 'CLASS'  # Default level
    order_level = 'ORDERS'
    family_level = 'FAMILY'
    genus_level = 'GENUS'

    run_sam_list = []
    for file1 in file_name_list:
        for file2 in file_name_list:
            checking_level = class_level
            if class_level in organism_hierarchy_dct[file1].keys() and class_level in \
                    organism_hierarchy_dct[file2].keys():

                if (organism_hierarchy_dct[file1][class_level] is None) or \
                        (organism_hierarchy_dct[file2][class_level] is None):
                    checking_level = order_level

                    if (organism_hierarchy_dct[file1][order_level] is None) or \
                            (organism_hierarchy_dct[file2][order_level] is None):
                        checking_level = family_level

                        if (organism_hierarchy_dct[file1][family_level] is None) or \
                                (organism_hierarchy_dct[file2][family_level] is None):
                            checking_level = genus_level

                if organism_hierarchy_dct[file1][checking_level] == organism_hierarchy_dct[file2][checking_level]:
                    if file1 != file2:
                        output_filename = "{}__{}.out".format(file1, file2)
                        if output_filename not in uploaded_sam_file_list:
                            logger.info(output_filename)
                            sam_file_path = os.path.join(path, output_filename)
                            file1_path = os.path.join(path, file1)
                            file2_path = os.path.join(path, file2)
                            run_sam_list.append(sam_file_path)
                            external_program.run_lastz(program, file1_path, file2_path, sam_file_path, logger)

    return run_sam_list


def parse_sam(sam_file, sam_id, parsed_sam_fh):
    """This function parse a SAM formatted fill and return data base format file """
    read_fh = open(sam_file, 'r')
    for i, line in enumerate(read_fh):
        if re.search(r'^@', line):
            continue
        if re.search(r'^#', line):
            continue
        tmp = re.split(r'\t', line)
        if len(tmp) < 8:
            print("Please check your SAM flie.")
        if len(tmp) > 8:
            # query_name = tmp[0]
            # ref_name = tmp[2]
            query_name, query_taxonomy_id, query_org_version = tmp[0].split('_', 3)
            ref_name, ref_taxonomy_id, ref_org_version = tmp[2].split('_', 3)

            ref_start = int(tmp[3])
            cigar_string = tmp[5]

            sequence = tmp[9]
            ref_len = len(sequence)
            (count_m, count_d, count_i, start_query) = process_cigar_string(cigar_string)
            query_end = start_query + ref_len
            ref_end = ref_start + ref_len - count_i

            # id_percentage = (count_i + count_d)*100 / ref_len

            sam_string1 = "{}\t{}\t{}\t{}".format(query_name, ref_name, query_taxonomy_id, query_org_version)
            sam_string2 = "{}\t{}\t{}\t{}\t{}".format(ref_taxonomy_id, ref_org_version, 0, 0, cigar_string)
            sam_string3 = "{}\t{}\t{}\t{}\t{}".format(start_query, query_end, ref_start, ref_end, count_m)
            sam_string4 = "{}\t{}\t{}\tNULL".format(0, 0, ref_len)
            sam_id += 1
            final_sam = "{}\t{}\t{}\t{}\t{}\n".format(sam_id, sam_string1, sam_string2, sam_string3, sam_string4)
            parsed_sam_fh.write(final_sam)
    return sam_id


def process_cigar_string(cigar_string):
    """
    This function parse a cigar string from SAM file
    It returns (count m, count I, count D and start query position)
    """
    pattern = re.compile("([0-9]+)([A-Za-z])")
    dct = collections.defaultdict(list)
    for number, letter in pattern.findall(cigar_string):
        dct[letter].append(number)

    m_data = dct.get('M', [0])
    d_data = dct.get('D', [0])
    i_data = dct.get('I', [0])
    h_data = dct.get('H', [1])
    count_m = sum(int(i) for i in m_data)
    count_d = sum(int(i) for i in d_data)
    count_i = sum(int(i) for i in i_data)
    start_query = int(h_data[0])
    return count_m, count_d, count_i, start_query


def sam_fasta_file_name(sam_path, data_list):

    filename = "{}_{}.fasta".format(data_list['TAXON_ID'], data_list['SEQUENCE_VERSION'])
    file_path = os.path.join(sam_path, filename)


def create_sam_alignment_directory(upload_path):
    """It creates the SamAlignment directory for SAM alignment program"""
    directory_name = "SamAlignment"
    sam_directory = os.path.join(upload_path, directory_name)
    if not os.path.exists(sam_directory):
        try:
            os.makedirs(sam_directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    return sam_directory


def get_sam_parsed_file_name(sam_path):
    """It returns the parsed_sam_file path """
    filename = "parsed_sam_file"
    parsed_sam_file = os.path.join(sam_path, filename)
    return parsed_sam_file


def upload_sam_data(db_config, sam_data):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 1)

    # For NASequenceImp table
    sql_1 = """LOAD DATA LOCAL INFILE '%s' INTO TABLE SamAlignment FIELDS TERMINATED BY '\t' OPTIONALLY
        ENCLOSED BY '"' LINES TERMINATED BY '\n';""" % sam_data
    print(sql_1)
    db_dots.insert(sql_1)


def find_uploaded_sam_files(db_config, path):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)

    sql_query = "SELECT query_taxon_id, query_organism_version, target_taxon_id, target_organism_version " \
                "FROM SamAlignment " \
                "group by query_taxon_id, query_organism_version, target_taxon_id, target_organism_version"
    result = db_dots.query(sql_query)

    file_list = []
    for i, value in enumerate(result):
        query_filename = "{}_{}.fasta".format(value['query_taxon_id'], value['query_organism_version'])
        target_filename = "{}_{}.fasta".format(value['target_taxon_id'], value['target_organism_version'])
        sam_file_name = '{}__{}.out'.format(query_filename, target_filename)
        file_list.append(sam_file_name)
    return file_list


def get_organism_hierarchy_map(db_config):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)
    sql_query = "SELECT * FROM Organism"
    result = db_dots.query(sql_query)
    hierarchy_dct = defaultdict(lambda: defaultdict())
    for i, value in enumerate(result):
        key = "{}_{}.fasta".format(value['TAXON_ID'], value['VERSION'])
        hierarchy_dct[key]['GENUS'] = value['GENUS']
        hierarchy_dct[key]['PHYLUM'] = value['PHYLUM']

        if value['FAMILY'] == 'None':
            hierarchy_dct[key]['FAMILY'] = None
        else:
            hierarchy_dct[key]['FAMILY'] = value['FAMILY']

        if value['ORDERS'] == 'None':
            hierarchy_dct[key]['ORDERS'] = None
        else:
            hierarchy_dct[key]['ORDERS'] = value['ORDERS']

        if value['CLASS'] == 'None':
            hierarchy_dct[key]['CLASS'] = None
        else:
            hierarchy_dct[key]['CLASS'] = value['CLASS']

    return hierarchy_dct
