import re
from collections import defaultdict, OrderedDict


def dct_structure():
    return defaultdict(dct_structure)


def read_gff3_genbank(gff_file):
    """
    This function takes gff file as input and return a dictionary of the gff file
    """
    dct = dct_structure()
    gene_id_dct = dct_structure()
    pseudo_gene_id_dct = dct_structure()

    read_fh = open(gff_file, 'r', encoding="utf-8")
    lookup_list = ['pseudogene', 'gene', 'mRNA', 'cds', 'exon', 'transcript']
    for i, line in enumerate(read_fh):
        line = line.rstrip()
        if re.search(r'^#', line):
            continue
        tmp = re.split(r'\t', line)

        if len(tmp) > 7:
            if any(item.lower() == tmp[2].lower() for item in lookup_list):
                source = tmp[0]
                match_obj = re.search(r'^(\S+) (.*)', tmp[0])
                if match_obj:
                    source = match_obj.group(1)

                if re.search(r'pseudogene', tmp[2], re.I):
                    dct, pseudo_gene_id_dct = process_gff_pseudogene_gene_line(dct, tmp, pseudo_gene_id_dct)
                elif re.search(r'gene', tmp[2], re.I):
                    dct = process_gff_gene_line(dct, tmp)

                if re.search(r'mrna', tmp[2], re.I):
                    dct, gene_id_dct = process_gff_mrna_line(dct, tmp, gene_id_dct, pseudo_gene_id_dct)

                if re.search(r'transcript', tmp[2], re.I):
                    dct, gene_id_dct = process_augustus_transcript_line(dct, tmp, gene_id_dct, pseudo_gene_id_dct)

                if re.search(r'cds', tmp[2], re.I):
                    super_parent_id, parent_id = get_cds_parent_data(tmp, gene_id_dct, source)
                    if super_parent_id in dct[source]['pseudogene']:
                        try:
                            dct[source]['pseudogene'][super_parent_id]['mrna'][parent_id]['cds']['location'].append(
                                [tmp[3], tmp[4]])
                        except AttributeError:
                            dct[source]['pseudogene'][super_parent_id]['mrna'][parent_id]['cds']['location'] = [
                                [tmp[3], tmp[4]]]
                    else:
                        try:
                            dct[source]['gene'][super_parent_id]['mrna'][parent_id]['cds']['location'].append([tmp[3], tmp[4]])
                        except AttributeError:
                            dct[source]['gene'][super_parent_id]['mrna'][parent_id]['cds']['location'] = [[tmp[3], tmp[4]]]

                if re.search(r'exon', tmp[2], re.I):
                    super_parent_id, parent_id = get_exon_parent_data(tmp, gene_id_dct, source)
                    if super_parent_id is not None and parent_id is not None:
                        if super_parent_id in pseudo_gene_id_dct:
                            try:
                                dct[source]['pseudogene'][super_parent_id]['mrna'][parent_id]['exon']['location'].append([tmp[3], tmp[4]])
                            except AttributeError:
                                dct[source]['pseudogene'][super_parent_id]['mrna'][parent_id]['exon']['location'] = [[tmp[3], tmp[4]]]
                        else:
                            try:
                                dct[source]['gene'][super_parent_id]['mrna'][parent_id]['exon']['location'].append([tmp[3], tmp[4]])
                            except AttributeError:
                                dct[source]['gene'][super_parent_id]['mrna'][parent_id]['exon']['location'] = [[tmp[3], tmp[4]]]

    return dct


def get_cds_parent_data(cds_line_list, gene_id_dct, source):
    attribute_dct = parse_single_feature_line(cds_line_list[8])
    super_parent_id, parent_id = None, None
    if 'parent' in attribute_dct:
        parent_id = attribute_dct['parent']
        if parent_id in gene_id_dct[source]:
            super_parent_id = gene_id_dct[source][parent_id]
        else:
            super_parent_id = parent_id
            parent_id = 'rna' + str(1)

    elif 'transcript_id' in attribute_dct:
        parent_id = attribute_dct['transcript_id']
        super_parent_id = attribute_dct['gene_id']

    return super_parent_id, parent_id


def get_exon_parent_data(exon_line_list, gene_id_dct, sequence_id):
    attribute_dct = parse_single_feature_line(exon_line_list[8])
    super_parent_id, parent_id = None, None

    if 'parent' in attribute_dct:
        parent_id = attribute_dct['parent']
        if parent_id in gene_id_dct[sequence_id]:
            super_parent_id = gene_id_dct[sequence_id][parent_id]
    elif 'transcript_id' in attribute_dct:
        parent_id = attribute_dct['transcript_id']
        super_parent_id = attribute_dct['gene_id']

    return super_parent_id, parent_id


def process_gff_gene_line(dct, tmp):

    attribute_dct = parse_single_feature_line(tmp[8])

    gff_attribute = GffAttribute()
    if not attribute_dct:
        gene_id = tmp[8]
    elif gff_attribute.id in attribute_dct:
        gene_id = attribute_dct[gff_attribute.id]
    else:
        raise Exception('Please check your Gff file')

    source = tmp[0]
    match_obj = re.search(r'^(\S+) (.*)', tmp[0])
    if match_obj:
        source = match_obj.group(1)

    try:
        dct[source]['gene'][gene_id]['location'].append([tmp[3], tmp[4], tmp[6]])
    except AttributeError:
        dct[source]['gene'][gene_id]['location'] = [[tmp[3], tmp[4], tmp[6]]]

    return dct


def process_gff_pseudogene_gene_line(dct, tmp, pseudo_gene_id_dct):
    attribute_dct = parse_single_feature_line(tmp[8])

    gff_attribute = GffAttribute()
    if not attribute_dct:
        gene_id = tmp[8]
    elif gff_attribute.id in attribute_dct:
        gene_id = attribute_dct[gff_attribute.id]
    else:
        raise Exception('Please check your Gff file')

    source = tmp[0]
    match_obj = re.search(r'^(\S+) (.*)', tmp[0])
    if match_obj:
        source = match_obj.group(1)

    pseudo_gene_id_dct[gene_id] = 'pseudogene'
    try:
        dct[source]['pseudogene'][gene_id]['location'].append([tmp[3], tmp[4], tmp[6]])
    except AttributeError:
        dct[source]['pseudogene'][gene_id]['location'] = [[tmp[3], tmp[4], tmp[6]]]

    return dct, pseudo_gene_id_dct


def process_gff_mrna_line(dct, tmp, gene_id_dct, pseudo_gene_id_dct):
    source = tmp[0]

    match_obj = re.search(r'^(\S+) (.*)', tmp[0])
    if match_obj:
        source = match_obj.group(1)

    attribute_dct = parse_single_feature_line(tmp[8])
    gff_attribute = GffAttribute()
    rna_id = None
    if gff_attribute.id in attribute_dct:
        rna_id = attribute_dct[gff_attribute.id]

    if gff_attribute.parent in attribute_dct and rna_id:
        gene_id = attribute_dct[gff_attribute.parent]
        gene_id_dct[source][rna_id] = gene_id
        if gene_id in pseudo_gene_id_dct:
            try:
                dct[source]['pseudogene'][gene_id]['mrna'][rna_id]['location'].append([tmp[3], tmp[4]])
            except AttributeError:
                dct[source]['pseudogene'][gene_id]['mrna'][rna_id]['location'] = [[tmp[3], tmp[4]]]
            if gff_attribute.product in attribute_dct:
                dct[source]['pseudogene'][gene_id]['mrna'][rna_id]['product'] = attribute_dct[gff_attribute.product]
        else:
            try:
                dct[source]['gene'][gene_id]['mrna'][rna_id]['location'].append([tmp[3], tmp[4]])
            except AttributeError:
                dct[source]['gene'][gene_id]['mrna'][rna_id]['location'] = [[tmp[3], tmp[4]]]

                if gff_attribute.product in attribute_dct:
                    dct[source]['gene'][gene_id]['mrna'][rna_id]['product'] = attribute_dct[gff_attribute.product]
    return dct, gene_id_dct


def process_augustus_transcript_line(dct, tmp, gene_id_dct, pseudo_gene_id_dct):
    attribute_dct = parse_single_feature_line(tmp[8])
    source = tmp[0]
    if not attribute_dct:
        arr = tmp[8].split('.')
        gene_id = arr[0]
        rna_id = tmp[8]
        gene_id_dct[source][tmp[8]] = arr[0]
        try:
            dct[source]['gene'][gene_id]['mrna'][rna_id]['location'].append([tmp[3], tmp[4]])
        except AttributeError:
            dct[source]['gene'][gene_id]['mrna'][rna_id]['location'] = [[tmp[3], tmp[4]]]
    else:
        dct, gene_id_dct = process_gff_mrna_line(dct, tmp, gene_id_dct, pseudo_gene_id_dct)

    return dct, gene_id_dct


class GffAttribute:
    product = 'product'
    id = 'id'
    parent = 'parent'


def parse_single_feature_line(attribute_string):
    # print(attribute_string)
    attributes = dict()
    for key_value_pair in attribute_string.split(';'):
        if not key_value_pair:
            # empty string due to a trailing ";"
            continue

        if "=" in key_value_pair:
            sub_attributes = key_value_pair.strip().split("=")
            if len(sub_attributes) == 1:
                attributes[sub_attributes[0].lower()] = None
            elif len(sub_attributes) == 2:
                attributes[sub_attributes[0].lower()] = sub_attributes[1]
            else:
                attributes[sub_attributes[0].lower()] = " ".join(sub_attributes[1:])
        elif " " in key_value_pair:
            key_value_pair = key_value_pair.strip()
            key, val = key_value_pair.split(" ", maxsplit=1)
            val = val.strip('"')
            attributes[key.lower()] = val
    return attributes


def make_custom_order(dct):
    sort_order = ['gene', 'mrna', 'cds', 'exon']

    all_sites_ordered = OrderedDict(OrderedDict(sorted(dct.items(), key=lambda i: sort_order.index(i[0]))))
    return all_sites_ordered


def make_custom_sort(orders):
    orders = [{k: -i for (i, k) in enumerate(reversed(order), 1)} for order in orders]

    def process(stuff):
        if isinstance(stuff, dict):
            l = [(k, process(v)) for (k, v) in stuff.items()]
            keys = set(stuff)
            for order in orders:
                if keys.issuperset(order):
                    return OrderedDict(sorted(l, key=lambda x: order.get(x[0], 0)))
            return OrderedDict(sorted(l))
        if isinstance(stuff, list):
            return [process(x) for x in stuff]
        return stuff
    return process
