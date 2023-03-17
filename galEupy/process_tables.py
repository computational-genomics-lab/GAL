import logging
from .dbtable_utility import TableUtility
_logger = logging.getLogger("galEupy.process_tables")


class TableProcessUtility(TableUtility):
    def __init__(self, db_dots, upload_dir, organism, taxonomy_id, version):
        TableUtility.__init__(self, db_dots, upload_dir, organism, taxonomy_id, version)

    def process_gff_gene_data(self, scaffold, gene_id, gene_dct, scaffold_na_sequence_id):
        gene_name = self.prefix + gene_id
        gene_data = GeneInfo(gene_name, gene_dct)
        self.na_sequenceimp_gene(self.NaSequenceId, scaffold, scaffold_na_sequence_id, gene_data)
        data_type = 'gene'
        self.na_featureimp(self.NaFeatureId, self.NaSequenceId, data_type, gene_name, "NULL")
        self.na_location(self.na_location_Id, self.NaFeatureId, gene_data.gene_start, gene_data.gene_end,
                         gene_data.strand)
        gene_na_feature_id = self.NaFeatureId
        self.NaFeatureId += 1
        self.na_location_Id += 1
        if 'tRNA' in gene_dct:
            for rna_id, rna_dct in gene_dct['tRNA'].items():
                data_type = 'tRNA'
                self.process_other_rna_data(rna_id, rna_dct, data_type, gene_na_feature_id, gene_data)

        if 'rRNA' in gene_dct:
            for rna_id, rna_dct in gene_dct['rRNA'].items():
                data_type = 'rRNA'
                self.process_other_rna_data(rna_id, rna_dct, data_type, gene_na_feature_id, gene_data)

        if 'mrna' in gene_dct:
            for rna_id, rna_dct in gene_dct['mrna'].items():
                data_type = 'mRNA'
                self.na_featureimp(self.NaFeatureId, self.NaSequenceId, data_type, rna_id, gene_na_feature_id)
                rna_data = RnaInfo(rna_dct)
                self.na_location(self.na_location_Id, self.NaFeatureId, rna_data.start, rna_data.end, gene_data.strand)

                if 'product' in rna_dct:
                    annotation = rna_dct['product']
                else:
                    annotation = 'Hypothetical Protein'

                self.gene_instance(self.GeneInstanceId, self.NaFeatureId, annotation)

                if 'protein_sequence' in rna_dct:
                    protein_sequence = rna_dct['protein_sequence']
                else:
                    protein_sequence = ""

                self.protein(self.ProteinId, gene_name, annotation, self.GeneInstanceId, protein_sequence)

                rna_na_feature_id = self.NaFeatureId

                self.NaFeatureId += 1
                self.na_location_Id += 1
                self.GeneInstanceId += 1
                self.ProteinId += 1

                if 'exon' in rna_dct:
                    self.process_cds_exon_gff_data('exon', rna_dct['exon'], rna_id, gene_data.strand, rna_na_feature_id)
                if 'cds' in rna_dct:
                    self.process_cds_exon_gff_data('cds', rna_dct['cds'], rna_id, gene_data.strand, rna_na_feature_id)

    def process_other_rna_data(self, rna_id, rna_dct, data_type, gene_na_feature_id, gene_data):
        rna_data = RnaInfo(rna_dct)
        self.na_featureimp_rna(self.NaFeatureId, self.NaSequenceId, data_type, rna_id, gene_na_feature_id)
        self.na_location(self.na_location_Id, self.NaFeatureId, rna_data.start, rna_data.end, gene_data.strand)
        self.NaFeatureId += 1
        self.na_location_Id += 1

    def process_cds_exon_gff_data(self, feature_name, feature_dct, rna_id, gene_strand, rna_na_feature_id):
        location = 'location'
        if location in feature_dct:
            for i in feature_dct[location]:
                if len(i) == 1:
                    feature_start = i[0]
                    feature_end = i[0]
                else:
                    feature_start = i[0]
                    feature_end = i[1]
                self.na_featureimp(self.NaFeatureId, self.NaSequenceId, feature_name, rna_id, rna_na_feature_id)
                self.na_location(self.na_location_Id, self.NaFeatureId, feature_start, feature_end, gene_strand)
                self.NaFeatureId += 1
                self.na_location_Id += 1

    def process_repeat_data(self, feature, feature_dct, scaffold_na_sequence_id):
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

                self.na_featureimp(self.NaFeatureId, scaffold_na_sequence_id, data_type, data_type, "NULL")
                self.na_location(self.na_location_Id, self.NaFeatureId, feature_start, feature_end, strand)

                self.NaFeatureId += 1
                self.na_location_Id += 1


'''

def process_gff_gene_data(gal_table, org_info, scaffold, gene_id, gene_dct, scaffold_na_sequence_id):
    gene_name = org_info.prefix + gene_id
    gene_data = GeneInfo(gene_name, gene_dct)
    today = get_date()
    na_sequence_imp_gene(gal_table, gal_table.NaSequenceId, org_info, scaffold, scaffold_na_sequence_id, gene_data, today)
    data_type = 'gene'
    na_feature_imp(gal_table, gal_table.NaFeatureId, gal_table.NaSequenceId, data_type, gene_name, "NULL")

    na_location(gal_table, gal_table.na_location_Id, gal_table.NaFeatureId, gene_data.gene_start, gene_data.gene_end,
                gene_data.strand)
    gene_na_feature_id = gal_table.NaFeatureId

    gal_table.NaFeatureId += 1
    gal_table.na_location_Id += 1

    if 'tRNA' in gene_dct:
        for rna_id, rna_dct in gene_dct['tRNA'].items():
            data_type = 'tRNA'
            process_other_rna_data(gal_table, gal_table, rna_id, rna_dct, data_type, gene_na_feature_id, gene_data)

    if 'rRNA' in gene_dct:
        for rna_id, rna_dct in gene_dct['rRNA'].items():
            data_type = 'rRNA'
            process_other_rna_data(gal_table, gal_table, rna_id, rna_dct, data_type, gene_na_feature_id, gene_data)

    if 'mrna' in gene_dct:
        for rna_id, rna_dct in gene_dct['mrna'].items():
            data_type = 'mRNA'
            na_feature_imp(gal_table, gal_table.NaFeatureId, gal_table.NaSequenceId, data_type, rna_id, gene_na_feature_id)

            rna_data = RnaInfo(rna_dct)

            na_location(gal_table, gal_table.na_location_Id, gal_table.NaFeatureId, rna_data.start, rna_data.end,
                                 gene_data.strand)

            if 'product' in rna_dct:
                annotation = rna_dct['product']
            else:
                annotation = 'Hypothetical Protein'

            gene_instance(gal_table, gal_table.GeneInstanceId, gal_table.NaFeatureId, annotation, today)

            if 'protein_sequence' in rna_dct:
                protein_sequence = rna_dct['protein_sequence']
            else:
                protein_sequence = ""
            protein(gal_table, gal_table.ProteinId, gene_name, annotation, gal_id.GeneInstanceId, protein_sequence)

            rna_na_feature_id = gal_table.NaFeatureId

            gal_table.NaFeatureId += 1
            gal_table.na_location_Id += 1
            gal_table.GeneInstanceId += 1
            gal_table.ProteinId += 1

            if 'exon' in rna_dct:
                process_cds_exon_gff_data(gal_table, gal_table, 'exon', rna_dct['exon'], rna_id, gene_data.strand,
                                          rna_na_feature_id)
            if 'cds' in rna_dct:
                process_cds_exon_gff_data(gal_table, gal_table, 'cds', rna_dct['cds'], rna_id, gene_data.strand,
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


def process_repeat_data(gal_table, feature, feature_dct, scaffold_na_sequence_id):
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

            na_feature_imp(gal_table, gal_table.NaFeatureId, scaffold_na_sequence_id, data_type, data_type, "NULL")
            na_location(gal_table, gal_table.na_location_Id, gal_table.NaFeatureId, feature_start, feature_end, strand)

            gal_table.NaFeatureId += 1
            gal_table.na_location_Id += 1
'''


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
        except ValueError:
            print(gene_dct['location'])
            print(gene_name, gene_dct)

