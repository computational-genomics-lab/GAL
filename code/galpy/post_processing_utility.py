from galpy import basic_utility as bu
import json


def create_gal_model_dct(sequence_dct, gff_dct, blast_dct={}):

    model_dct = gff_dct
    delete_list = []
    for seq_id, sequence in sequence_dct.items():
        if seq_id in gff_dct:
            if 'gene' in gff_dct[seq_id]:
                for gene_id, gene_dct in gff_dct[seq_id]['gene'].items():
                    if gene_id is None:
                        delete_list.append([seq_id, 'gene', gene_id])
                        continue
                    try:
                        gene_sequence, strand = get_gene_sequence(sequence, gene_dct['location'])
                    except (RuntimeError, TypeError, NameError, ValueError):
                        # print(json.dumps(gene_dct['location'], indent=4))
                        print("Warning Check: %s" % gene_id)
                        # print(json.dumps(gene_dct, indent=4))
                        break

                    # Add gene sequence in the feature dictionary
                    model_dct[seq_id]['gene'][gene_id]['gene_sequence'] = gene_sequence

                    if 'mrna' in gene_dct:
                        # for each mrna id
                        for rna_id, rna_dct in gene_dct['mrna'].items():
                            if blast_dct:
                                if 'product' not in rna_dct:
                                    if rna_id in blast_dct:
                                        product = blast_dct[rna_id]
                                    else:
                                        product = "Hypothetical Protein"

                                    model_dct[seq_id]['gene'][gene_id]['mrna'][rna_id]['product'] = product

                            if 'cds' in rna_dct:
                                location_list = rna_dct['cds']['location']
                                if 'protein_sequence' not in rna_dct:

                                    merged_cds = merge_cds_list(sequence, location_list, strand)
                                    protein_seq = bu.translate(merged_cds)
                                    model_dct[seq_id]['gene'][gene_id]['mrna'][rna_id]['protein_sequence'] = protein_seq

                            if 'exon' not in rna_dct:
                                model_dct[seq_id]['gene'][gene_id]['mrna'][rna_id]['exon'] = rna_dct['cds']

                            if 'location' not in rna_dct:
                                if 'cds' in rna_dct:
                                    location_list = rna_dct['cds']['location']
                                    location = get_start_end_list(location_list, strand)
                                    model_dct[seq_id]['gene'][gene_id]['mrna'][rna_id]['location'] = location
                                else:
                                    model_dct[seq_id]['gene'][gene_id]['mrna'][rna_id]['location'] = gene_dct['location']

    for del_list in delete_list:
        del model_dct[del_list[0]][del_list[1]][del_list[2]]
    return model_dct


def get_start_end_list(location_list, strand):
    sorted_location_list = sorted(location_list)
    start = sorted_location_list[0][0]
    end = sorted_location_list[-1][-1]
    location = [[start, end, strand]]
    return location


def merge_cds_list(sequence, location_list, strand):
    sorted_location_list = sorted(location_list)
    cds_sequence = ''
    for i, location in enumerate(sorted_location_list):
        if len(location) == 1:
            start_cds = int(location[0])-1
            end_cds = int(location[0]) - 1
        else:
            start_cds = int(location[0])-1
            end_cds = int(location[1])-1

        if start_cds < end_cds:
            cds_sequence = cds_sequence + sequence[start_cds:end_cds]
        else:
            cds_sequence = cds_sequence + sequence[end_cds:start_cds]
    if strand == '-':
        cds_sequence = bu.reverse_complement(cds_sequence)

    return cds_sequence


def get_gene_sequence(sequence, location_list):

    start_location, end_location, strand = location_list[0]

    start_location = int(start_location)-1
    end_location = int(end_location)-1
    if start_location < end_location:
        gene_sequence = sequence[start_location:end_location]
    else:
        gene_sequence = sequence[end_location:start_location]

    if strand == '-':
        gene_sequence = bu.reverse_complement(gene_sequence)

    return gene_sequence, strand


def fix_multiple_splicing_bugs(feature_data_dct):
    level_to_del = []
    for locus_name, locus_dct in feature_data_dct.items():
        for feature_name, feature_dct in locus_dct.items():
            if feature_name == 'gene':
                for gene_id, gene_dct in feature_dct.items():
                    for gene_feature, gene_feature_dct in gene_dct.items():
                        if gene_feature == 'mrna':
                            for feature_id, feature_id_dct in gene_feature_dct.items():
                                if 'cds' not in feature_id_dct:
                                    level_to_del.append((locus_name, feature_name, gene_id, gene_feature, feature_id))

    for lvl1, lvl2, lvl3, lvl4, lvl5 in level_to_del:
        feature_data_dct[lvl1][lvl2][lvl3][lvl4].pop(lvl5, None)

    return feature_data_dct
