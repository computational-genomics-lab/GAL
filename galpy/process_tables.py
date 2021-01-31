import logging
from .generalutility import get_date
from .dbtableutility import na_sequence_imp_gene, na_feature_imp, na_location, gene_instance, na_feature_imp_rna
from .dbtableutility import protein
_logger = logging.getLogger("galpy.process_tables")


def process_gff_gene_data(gal_id, gal_fh, org_info, scaffold, gene_id, gene_dct, scaffold_na_sequence_id):
    gene_name = org_info.prefix + gene_id
    gene_data = GeneInfo(gene_name, gene_dct)
    today = get_date()
    na_sequence_imp_gene(gal_fh, gal_id.NaSequenceId, org_info, scaffold, scaffold_na_sequence_id, gene_data, today)
    data_type = 'gene'
    na_feature_imp(gal_fh, gal_id.NaFeatureId, gal_id.NaSequenceId, data_type, gene_name, "NULL")

    na_location(gal_fh, gal_id.na_location_Id, gal_id.NaFeatureId, gene_data.gene_start, gene_data.gene_end,
                gene_data.strand)
    gene_na_feature_id = gal_id.NaFeatureId

    gal_id.NaFeatureId += 1
    gal_id.na_location_Id += 1

    if 'tRNA' in gene_dct:
        for rna_id, rna_dct in gene_dct['tRNA'].items():
            data_type = 'tRNA'
            process_other_rna_data(gal_fh, gal_id, rna_id, rna_dct, data_type, gene_na_feature_id, gene_data)

    if 'rRNA' in gene_dct:
        for rna_id, rna_dct in gene_dct['rRNA'].items():
            data_type = 'rRNA'
            process_other_rna_data(gal_fh, gal_id, rna_id, rna_dct, data_type, gene_na_feature_id, gene_data)

    if 'mrna' in gene_dct:
        for rna_id, rna_dct in gene_dct['mrna'].items():
            data_type = 'mRNA'
            na_feature_imp(gal_fh, gal_id.NaFeatureId, gal_id.NaSequenceId, data_type, rna_id, gene_na_feature_id)

            rna_data = RnaInfo(rna_dct)

            na_location(gal_fh, gal_id.na_location_Id, gal_id.NaFeatureId, rna_data.start, rna_data.end,
                                 gene_data.strand)

            if 'product' in rna_dct:
                annotation = rna_dct['product']
            else:
                annotation = 'Hypothetical Protein'

            gene_instance(gal_fh, gal_id.GeneInstanceId, gal_id.NaFeatureId, annotation, today)

            if 'protein_sequence' in rna_dct:
                protein_sequence = rna_dct['protein_sequence']
            else:
                protein_sequence = ""
            protein(gal_fh, gal_id.ProteinId, gene_name, annotation, gal_id.GeneInstanceId, protein_sequence)

            rna_na_feature_id = gal_id.NaFeatureId

            gal_id.NaFeatureId += 1
            gal_id.na_location_Id += 1
            gal_id.GeneInstanceId += 1
            gal_id.ProteinId += 1

            if 'exon' in rna_dct:
                process_cds_exon_gff_data(gal_id, gal_fh, 'exon', rna_dct['exon'], rna_id, gene_data.strand,
                                          rna_na_feature_id)
            if 'cds' in rna_dct:
                process_cds_exon_gff_data(gal_id, gal_fh, 'cds', rna_dct['cds'], rna_id, gene_data.strand,
                                          rna_na_feature_id)


def process_other_rna_data(gal_fh, gal_id, rna_id, rna_dct, data_type, gene_na_feature_id, gene_data):
    rna_data = RnaInfo(rna_dct)
    na_feature_imp_rna(gal_fh, gal_id.NaFeatureId, gal_id.NaSequenceId, data_type, rna_id, gene_na_feature_id)
    na_location(gal_fh, gal_id.na_location_Id, gal_id.NaFeatureId, rna_data.start, rna_data.end, gene_data.strand)
    gal_id.NaFeatureId += 1
    gal_id.na_location_Id += 1


def process_cds_exon_gff_data(gal_id, gal_fh, feature_name, feature_dct, rna_id, gene_strand, rna_na_feature_id):
    location = 'location'
    if location in feature_dct:
        for i in feature_dct[location]:
            if len(i) == 1:
                feature_start = i[0]
                feature_end = i[0]
            else:
                feature_start = i[0]
                feature_end = i[1]
            na_feature_imp(gal_fh, gal_id.NaFeatureId, gal_id.NaSequenceId, feature_name, rna_id, rna_na_feature_id)
            na_location(gal_fh, gal_id.na_location_Id, gal_id.NaFeatureId, feature_start, feature_end, gene_strand)
            gal_id.NaFeatureId += 1
            gal_id.na_location_Id += 1


def process_repeat_data(gal_id, gal_fh, feature, feature_dct, scaffold_na_sequence_id):
    data_type = feature
    location = 'location'
    if location in feature_dct:
        for i in feature_dct[location]:
            if len(i) == 1:
                feature_start = i[0]
                feature_end = i[0]
            else:
                feature_start = i[0]
                feature_end = i[1]
            if feature_start < feature_end:
                strand = 0
            else:
                strand = 1

            na_feature_imp(gal_fh, gal_id.NaFeatureId, scaffold_na_sequence_id, data_type, data_type, "NULL")
            na_location(gal_fh, gal_id.na_location_Id, gal_id.NaFeatureId, feature_start, feature_end, strand)

            gal_id.NaFeatureId += 1
            gal_id.na_location_Id += 1


class RnaInfo:
    def __init__(self, rna_dct):
        location_list = rna_dct['location'][0]
        self.start = location_list[0]
        self.end = location_list[1]


class GeneInfo:
    def __init__(self, gene_name, gene_dct):
        self.gene_name = gene_name
        self.gene_sequence = gene_dct['gene_sequence']
        try:
            self.gene_start, self.gene_end, strand = gene_dct['location'][0]
            if strand == '-':
                self.strand = 1
            else:
                self.strand = 0
        except:
            print(gene_dct['location'])
            print(gene_name, gene_dct)

