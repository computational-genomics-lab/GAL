import re
from collections import defaultdict, OrderedDict
import sys, json
import logging
_logger = logging.getLogger("galpy.BioFile.genbank_parser")

def default_dct_structure():
    return defaultdict(default_dct_structure)


def get_data(fp_in):
    dna_beg_pos = 0
    data_store = []
    locus_flag = 0
    gene_flag = 0
    gene_count = 0
    sequence_dct = {}
    dna_array = []
    locus_dct = default_dct_structure()
    product_dct = default_dct_structure()
    transcript_id_dct = {}
    for i, data in enumerate(fp_in):
        # This Part is for header part: start
        if type(data) == bytes:
            data = data.decode()

        if re.match("^LOCUS ", data):
            data_store = []
            locus_flag = 1

        if locus_flag == 1:
            data_store.append(data)

        if re.match("^FEATURES ", data):
            locus_flag = 0
            locus = HeaderScan(data_store)
            data_store = []

        # Parsing gene feature start
        if re.match("^ {5}(gene)", data) and locus:
            gene_count += 1
            if gene_flag == 0:
                gene_flag = 1
            else:
                locus_dct, transcript_id_dct, product_dct = process_single_gene_data(data_store, transcript_id_dct,
                                                                                     locus_dct, locus.Name, product_dct)
                data_store = []
        if gene_flag == 1:
            data_store.append(data)
        # match the end of dna sequence
        if re.match("^//\n", data):
            sequence_string = ''.join(dna_array)
            sequence_dct[locus.Name] = sequence_string
            dna_array = []
            dna_beg_pos = 0

        if dna_beg_pos == 1:
            data = re.sub(r'\d', "", data.rstrip())
            data = re.sub(r' ', "", data)
            dna_array.append(data)

        # match the beginning of dna sequence
        if re.match("^ORIGIN", data):
            dna_beg_pos = 1
            locus_dct, transcript_id_dct, product_dct = process_single_gene_data(data_store, transcript_id_dct,
                                                                                 locus_dct, locus.Name, product_dct)

            data_store = []
    return locus_dct, sequence_dct


def process_single_gene_data(gene_data, transcript_id_dct, locus_dct, locus_name, product_dct):
    feature_key_indent = 5
    feature_qualifier_indent = 21

    feature_key_spacer = " " * feature_key_indent
    key_regex = r"^" + feature_key_spacer + r"\w"
    feature_key_flag = 0
    feature = []
    feature_store = []
    for i, data in enumerate(gene_data):
        if re.search(key_regex, data, re.IGNORECASE):
            if feature_key_flag == 1:
                feature_store.append(feature)
                feature = [data]
                if len(gene_data) == (i + 1):
                    feature_store.append(feature)
            else:
                feature_key_flag = 1
                feature.append(data)
        elif len(gene_data) == (i + 1):
            feature.append(data)
            feature_store.append(feature)
        else:
            feature.append(data)
    locus_dct, transcript_id_dct, product_dct = single_gene_data_to_dict(feature_store, transcript_id_dct,
                                                                         locus_dct, locus_name, product_dct)
    return locus_dct, transcript_id_dct, product_dct


def single_gene_data_to_dict(feature_store, transcript_id_dct, locus_dct, locus_name, product_dct):
    dct = convert_gene_record_to_dictionary_format(feature_store)

    gene_id = None
    transcript_id = None

    feature = 'repeat_region'
    if feature in dct:
        locus_dct = process_repeat_region_data(dct, locus_dct, locus_name, feature)

    feature = 'gene'
    if feature in dct:
        locus_dct, gene_id = process_gene_data(dct, locus_dct, locus_name)

    # if gene_id == 'LCAZH_RS00215' or gene_id == 'LCAZH_RS00220':
    #    print(feature_store)

    feature = 'tRNA'
    if feature in dct and gene_id:
        locus_dct, transcript_id, product_dct, transcript_id_dct = process_gff_other_rna_data(dct, locus_dct, gene_id,
                                                                                              transcript_id_dct,
                                                                                              locus_name,
                                                                                              product_dct, feature)
    feature = 'rRNA'
    if feature in dct and gene_id:
        locus_dct, transcript_id, product_dct, transcript_id_dct = process_gff_other_rna_data(dct, locus_dct, gene_id,
                                                                                              transcript_id_dct,
                                                                                              locus_name,
                                                                                              product_dct, feature)
    feature = 'mRNA'
    m_rna_count = 0
    if feature in dct and gene_id:
        m_rna_count = len(dct[feature])
        locus_dct, transcript_id, product_dct, transcript_id_dct = process_gff_m_rna_data(dct, locus_dct, gene_id,
                                                                                          transcript_id_dct, locus_name,
                                                                                          product_dct)

    feature = 'CDS'
    if feature in dct:
        cds_count = len(dct[feature])
        if m_rna_count == 0 and cds_count == 1:
            locus_dct = process_gff_cds_type1_data(dct, locus_dct, gene_id, transcript_id_dct, locus_name)

        elif m_rna_count == 1 and cds_count == 1 and transcript_id:
            locus_dct = process_gff_cds_type3_data(dct, locus_dct, gene_id, product_dct, locus_name, transcript_id)

        elif m_rna_count == cds_count > 1 and product_dct:
            locus_dct = process_gff_cds_type3_data(dct, locus_dct, gene_id, product_dct, locus_name, transcript_id)
        else:
            locus_dct = process_gff_cds_type3_data(dct, locus_dct, gene_id, product_dct, locus_name, transcript_id)

    return locus_dct, transcript_id_dct, product_dct


def convert_gene_record_to_dictionary_format(feature_store):
    dct = OrderedDict()
    for i, data in enumerate(feature_store):
        (feature_key, feature_line) = get_feature_key_qualifier(data)
        if feature_key in dct:
            dct[feature_key].append(feature_line)
        else:
            dct[feature_key] = [feature_line]
    return dct


def process_gene_data(gb_dct, gene_dct, locus_name):
    feature = 'gene'
    qualifier_dct, location, strand, start_loc, end_loc = extract_feature_record(feature, gb_dct[feature][0])
    gene_id = get_gene_name(qualifier_dct)
    try:
        gene_dct[locus_name]['gene'][gene_id]['location'].append([start_loc, end_loc, strand])
    except AttributeError:
        gene_dct[locus_name]['gene'][gene_id]['location'] = [[start_loc, end_loc, strand]]

    return gene_dct, gene_id


def process_gff_m_rna_data(gb_dct, gene_dct, prev_gene_id, transcript_id_dct, locus_name, product_dct):

    transcript_id = None
    feature = 'mRNA'
    for i in range(len(gb_dct[feature])):
        qualifier_dct, location, strand, start_loc, end_loc = extract_feature_record(feature, gb_dct[feature][i])
        gene_id, transcript_id = find_gene_id_and_transcript_id(qualifier_dct, transcript_id_dct)
        if gene_id is None:
            gene_id = prev_gene_id

        transcript_id_dct[transcript_id] = gene_id

        feature_name = 'mrna'
        if 'product' in qualifier_dct:
            gene_dct[locus_name]['gene'][gene_id][feature_name][transcript_id]['product'] = qualifier_dct['product']
            product_dct[gene_id][qualifier_dct['product']] = transcript_id

        try:
            gene_dct[locus_name]['gene'][gene_id][feature_name][transcript_id]['location'].append([start_loc, end_loc])
        except AttributeError:
            gene_dct[locus_name]['gene'][gene_id][feature_name][transcript_id]['location'] = [[start_loc, end_loc]]

        try:
            gene_dct[locus_name]['gene'][gene_id][feature_name][transcript_id]['exon']['location'].append(location)
        except AttributeError:
            gene_dct[locus_name]['gene'][gene_id][feature_name][transcript_id]['exon']['location'] = location

    return gene_dct, transcript_id, product_dct, transcript_id_dct


def process_gff_other_rna_data(gb_dct, gene_dct, prev_gene_id, transcript_id_dct, locus_name, product_dct, feature):

    transcript_id = None
    for i in range(len(gb_dct[feature])):
        qualifier_dct, location, strand, start_loc, end_loc = extract_feature_record(feature, gb_dct[feature][i])
        gene_id, transcript_id = find_gene_id_and_transcript_id(qualifier_dct, transcript_id_dct, None, feature)

        if gene_id is None:
            gene_id = prev_gene_id

        transcript_id_dct[transcript_id] = gene_id
        if 'product' in qualifier_dct:
            gene_dct[locus_name]['gene'][gene_id][feature][transcript_id]['product'] = qualifier_dct['product']
            product_dct[gene_id][qualifier_dct['product']] = transcript_id

        try:
            gene_dct[locus_name]['gene'][gene_id][feature][transcript_id]['location'].append([start_loc, end_loc])
        except AttributeError:
            gene_dct[locus_name]['gene'][gene_id][feature][transcript_id]['location'] = [[start_loc, end_loc]]

        return gene_dct, transcript_id, product_dct, transcript_id_dct


def process_gff_cds_type1_data(gb_dct, gene_dct, prev_gene_id, transcript_id_dct, locus_name):
    feature = 'CDS'
    qualifier_dct, location, strand, start_loc, end_loc = extract_feature_record(feature, gb_dct[feature][0])

    parent_feature = 'mrna'
    gene_id, transcript_id = find_gene_id_and_transcript_id(qualifier_dct, transcript_id_dct)
    if gene_id is None:
        gene_id = prev_gene_id

    if 'product' in qualifier_dct:
        gene_dct[locus_name]['gene'][gene_id][parent_feature][transcript_id]['product'] = qualifier_dct['product']

    try:
        gene_dct[locus_name]['gene'][gene_id][parent_feature][transcript_id]['location'].append([start_loc, end_loc])
    except AttributeError:
        gene_dct[locus_name]['gene'][gene_id][parent_feature][transcript_id]['location'] = [[start_loc, end_loc]]

    gene_dct[locus_name]['gene'][gene_id][parent_feature][transcript_id]['exon']['location'] = location
    gene_dct = add_cds_data_to_dictionary(gene_dct, qualifier_dct, gene_id, transcript_id, location, locus_name)

    return gene_dct


def process_gff_cds_type2_data(gb_dct, gene_dct, prev_gene_id, transcript_id, transcript_id_dct, locus_name):
    # cds count = 1 and m_rna count = 1
    feature = 'CDS'
    qualifier_dct, location, strand, start_loc, end_loc = extract_feature_record(feature, gb_dct[feature][0])

    gene_id, transcript_id = find_gene_id_and_transcript_id(qualifier_dct, transcript_id_dct, transcript_id)
    if gene_id is None:
        gene_id = prev_gene_id

    gene_dct = add_cds_data_to_dictionary(gene_dct, qualifier_dct, gene_id, transcript_id, location, locus_name)
    return gene_dct


def process_gff_cds_type3_data(gb_dct, gene_dct, prev_gene_id, product_dct, locus_name, transcript_id):
    # cds count = n and m_rna count = n

    cds_product_dct = defaultdict(list)
    feature = 'CDS'

    for i in range(len(gb_dct[feature])):
        qualifier_dct, location, strand, start_loc, end_loc = extract_feature_record(feature, gb_dct[feature][i])
        gene_id = get_gene_name(qualifier_dct)
        if gene_id is None:
            gene_id = prev_gene_id

        if 'product' in qualifier_dct:
            product_name = qualifier_dct['product']
            cds_product_dct[gene_id].append(product_name)

            cds_rna_match_dct = find_associated_id_using_string_comparision(product_dct[gene_id],
                                                                            cds_product_dct[gene_id])

            if product_name in cds_rna_match_dct:
                transcript_id = cds_rna_match_dct[product_name]
                gene_dct = add_cds_data_to_dictionary(gene_dct, qualifier_dct, gene_id, transcript_id,
                                                      location, locus_name)

        elif 'product' not in qualifier_dct and transcript_id:
            gene_dct = add_cds_data_to_dictionary(gene_dct, qualifier_dct, gene_id, transcript_id, location, locus_name)

    return gene_dct


def process_repeat_region_data(gb_dct, gene_dct, locus_name, feature):
    qualifier_dct, location, strand, start_loc, end_loc = extract_feature_record(feature, gb_dct[feature][0])
    try:
        gene_dct[locus_name][feature]['location'].append([start_loc, end_loc, strand])
    except AttributeError:
        gene_dct[locus_name][feature]['location'] = [[start_loc, end_loc, strand]]
    return gene_dct


def add_cds_data_to_dictionary(gene_dct, qualifier_dct, gene_id, transcript_id, location, locus_name):
    parent_feature = 'mrna'

    if 'translation' in qualifier_dct:
        gene_dct[locus_name]['gene'][gene_id][parent_feature][transcript_id]['protein_sequence'] =\
            qualifier_dct['translation']

    gene_dct[locus_name]['gene'][gene_id]['mrna'][transcript_id]['cds']['location'] = location

    return gene_dct


def find_gene_id_and_transcript_id(qualifier_dct, transcript_id_dct, m_rna_id=None, transcript_type='mrna'):
    gene_id = get_gene_name(qualifier_dct)
    transcript_id = get_rna_id(qualifier_dct)

    if transcript_type != 'mrna':
        transcript_id = gene_id
    elif transcript_id is None and m_rna_id is not None:
        transcript_id = m_rna_id
    elif transcript_id is None and m_rna_id is None:
        transcript_id = gene_id + '-mRNA'

    if transcript_id in transcript_id_dct:
        if transcript_id_dct[transcript_id] != gene_id:
            for transcript_key, gene_value in transcript_id_dct.items():
                if gene_value == gene_id:
                    transcript_id = transcript_key

    return gene_id, transcript_id


def extract_feature_record(feature_key, feature_array):
    (feature_key, location, feature_qualifier) = process_single_feature_data(feature_key, feature_array)
    (location, strand) = parse_location(location)
    qualifier_dct = transform_qualifier_dct(feature_qualifier)

    start_loc, end_loc = get_start_end_location(location)

    return qualifier_dct, location, strand, start_loc, end_loc


def find_associated_id_using_string_comparision(dct, string_list):
    match_dct = {}
    # match[cds_product] = m_rna_product
    for data in string_list:
        if data in dct:
            match_dct[data] = data
        else:
            data1 = data.replace('isoform', 'variant')
            if data1 in dct:
                match_dct[data] = data1
            else:
                string_finder = 'variant'
                m = re.search(string_finder, data1)
                if m:
                    string_matcher = data1[data1.index(string_finder):]
                    # print(string_matcher)
                    for key, value in dct.items():
                        if string_matcher in key:
                            match_dct[data] = key

    result_dct = {}
    length_diff = len(string_list) - len(match_dct)
    if length_diff == 0:
        for key, value in match_dct.items():
            result_dct[key] = dct[value]
    elif length_diff == 1:
        # find missing id in string_list
        missed_cds_id = ''
        for data in string_list:
            if data in match_dct:
                result_dct[data] = dct[match_dct[data]]
            else:
                missed_cds_id = data
        # find missing string in match_dct
        if missed_cds_id:
            for key, value in dct.items():
                if key not in match_dct.values():
                    result_dct[missed_cds_id] = value
    else:
        pass
        # print("Check the gene details")

    return result_dct


def get_start_end_location(location_list):
    start_location = location_list[0][0]
    end_location = location_list[-1][-1]

    return start_location, end_location


def get_rna_id(dct):
    qualifier_key_list = ['transcript_id']
    rna_id = retrieve_id(dct, qualifier_key_list)
    return rna_id


def get_gene_name(dct):
    qualifier_key_list = ['gene', 'locus_tag']
    gene_name = retrieve_id(dct, qualifier_key_list)
    return gene_name


def retrieve_id(dct, key_list):
    for data in key_list:
        if data in dct:
            return dct[data]


def transform_qualifier_dct(feature_qualifier):
    qualifier_dct = {}

    for data in feature_qualifier:
        if len(data) == 2:
            data = list(data)
            if data[0] == 'product':
                data[1] = data[1].replace('\n', ' ')
            elif data[1] is not None:
                data[1] = data[1].replace('\n', '')
            qualifier_dct[data[0]] = data[1]
    return qualifier_dct


def get_feature_key_qualifier(data_array):
    feature_ley_indent = 5
    feature_qualifier_indent = 21
    feature_key_space = " " * feature_ley_indent
    feature_qualifier_space = " " * feature_qualifier_indent

    feature_key = ''
    feature_lines = []

    try:
        for line in data_array:
            match_obj = re.match(r' {5}(\w+)', line, re.M | re.I)
            if match_obj:
                feature_key = match_obj.group(1)
                line = re.sub(r' +\w+ +', '', line)
                feature_lines.append(line.strip())
            if line[:feature_qualifier_indent] == feature_qualifier_space and (line != ''):
                feature_lines.append(line[feature_qualifier_indent:].strip())
        return feature_key, feature_lines
    except StopIteration:
        raise ValueError("Problem with feature:\n%s" % ("\n".join(data_array)))


def process_single_feature_data(feature_key, data_array):
    iterator = (x for x in data_array if x)
    try:
        line = next(iterator)

        feature_location = line.strip()
        while feature_location[-1:] == ",":
            line = next(iterator)
            feature_location += line.strip()
        if feature_location.count("(") > feature_location.count(")"):
            while feature_location[-1:] == "," or feature_location.count("(") > feature_location.count(")"):
                line = next(iterator)
                feature_location += line.strip()
        qualifiers = []
        for line_number, line in enumerate(iterator):
            if line_number == 0 and line.startswith(")"):
                feature_location += line.strip()
            elif line[0] == "/":
                i = line.find("=")
                key = line[1:i]
                value = line[i + 1:]
                if i == -1:
                    key = line[1:]
                    qualifiers.append((key, None))
                elif not value:
                    qualifiers.append((key, ""))
                elif value == '"':
                    qualifiers.append((key, value))
                elif value[0] == '"':
                    value_list = [value]
                    while value_list[-1][-1] != '"':
                        value_list.append(next(iterator))
                    value = '\n'.join(value_list)
                    value = re.sub('"', '', value)
                    qualifiers.append((key, value))
                else:
                    qualifiers.append((key, value))
            else:
                assert len(qualifiers) > 0
                assert key == qualifiers[-1][0]
                if qualifiers[-1][1] is None:
                    raise StopIteration
                qualifiers[-1] = (key, qualifiers[-1][1] + "\n" + line)

        return feature_key, feature_location, qualifiers

    except StopIteration:
        raise ValueError("Problem with '%s' feature:\n%s" % (feature_key, "\n".join(data_array)))


def parse_location(location):
    location_array = []
    _re_complement = re.compile(r"complement")
    _re_join = re.compile(r"join")
    _re_substitute = re.compile('[^0-9.,]')

    complement = _re_complement.search(location)
    if complement:
        stand = "-"
    else:
        stand = "+"
    join = _re_join.search(location)

    if join:
        # loc = re.sub(r'[^0-9\.,]', '', location)
        loc = _re_substitute.sub(r'', location)
        tmp = re.split(",", loc)
        for loc in tmp:
            val = re.split("\.\.", loc)
            location_array.append(val)
    else:
        # loc = re.sub(r'[^0-9\.,]', '', location)
        loc = _re_substitute.sub(r'', location)
        tmp = re.split("\.\.", loc)
        location_array.append(tmp)

    return location_array, stand


def open_input_file(input_filename):
    try:
        _logger.debug("Genbank file: {}".format(input_filename))
        fp_in = open(input_filename, "rb")
    except IOError as e:
        _logger.error("Genbank file: {}".format(input_filename))
        _logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(0)
    except ValueError:
        _logger.error("Could not convert data to an integer.")
        sys.exit(0)
    except:
        _logger.error("Unexpected error:", sys.exc_info()[0])
        raise
    return fp_in


class HeaderScan:
    def __init__(self, data_array):

        for i, data in enumerate(data_array):
            if re.match("^LOCUS", data):
                tmp = re.split(" +", data)
                self.Name = tmp[1]
                self.Length = tmp[2]
                self.Type = tmp[3]
                self.Topology = tmp[4]
                try:
                    self.DivisionCode = tmp[5]
                except IndexError:
                    self.DivisionCode = None
                try:
                    self.Date = tmp[6]
                except IndexError:
                    self.Date = None

            if re.match("^DEFINITION", data):
                tmp = re.split(" +", data)
                self.definition = tmp[1]

            if re.match("^ACCESSION", data):
                tmp = re.split(" +", data)
                self.accession = tmp[1]

            if re.match("^VERSION", data):
                tmp = re.split(" +", data)
                try:
                    self.version = tmp[1]
                except IndexError:
                    self.version = None

            if re.match("^SOURCE", data):
                tmp = re.split(" +", data)
                self.source = tmp[1]
