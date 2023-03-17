from galeupy import db_function
from galeupy import organism_function
from galeupy import directory_utility
from galeupy import external_program, logging_utility
from pathlib import PurePosixPath


def create_row_files(db_config, taxonomy_id, org_name, org_version, path_config, log_file):
    logger = logging_utility.logger_function(__name__, log_file)
    org_info = organism_function.OrganismInfo(org_name, taxonomy_id, org_version)
    upload_path = path_config.blast_path

    nucleotide_dir, protein_dir = directory_utility.create_blast_feature_directory(upload_path)

    genomic_seq_file = PurePosixPath(nucleotide_dir, org_info.org_short_name)
    protein_seq_file = PurePosixPath(protein_dir, org_info.org_short_name)

    db_dots = db_function.create_db_dots_connection(db_config)

    create_scaffold_sequence_file(db_dots, taxonomy_id, org_version, genomic_seq_file)
    create_protein_file(db_dots, taxonomy_id, org_version, protein_seq_file)
    db_creator_program = path_config.db_creator
    external_program.nucleotide_format_db(db_creator_program, genomic_seq_file, genomic_seq_file, logger)
    external_program.protein_format_db(db_creator_program, protein_seq_file, protein_seq_file, logger)


def create_scaffold_sequence_file(db_dots, taxonomy_id, org_version, genomic_seq_file):

    sql_query = 'select string1, sequence from NASequenceImp where taxon_id ={} and sequence_version={} and ' \
                'sequence_type_id=1'.format(taxonomy_id, org_version)
    out_file = open(genomic_seq_file, 'w')

    result = db_dots.query(sql_query)
    for i, value in enumerate(result):
        sequence = ">{}\n{}\n".format(value['string1'], value['sequence'])
        out_file.write(sequence)
    out_file.close()


def create_protein_file(db_dots, taxonomy_id, org_version, protein_seq_file):

    sql_query = """select nf.na_sequence_id, nf.name as transcript_name, p.sequence, en.string1 as 'source_id', 
    en.string3 as 'gene_name', gi.description, p.sequence
    from NASequenceImp en, NAFeatureImp nf, GeneInstance gi, Protein p
    where
    en.taxon_id = {} 
    and en.sequence_version ={}
    and en.sequence_type_id= 6 
    and nf.na_sequence_id = en.na_sequence_id
    and nf.feature_type='mRNA'
    and gi.na_feature_id = nf.na_feature_id
    and p.gene_instance_id = gi.gene_instance_id""".format(taxonomy_id, org_version)

    out_file = open(protein_seq_file, 'w')

    result = db_dots.query(sql_query)
    for i, value in enumerate(result):
        sequence = ">{}\n{}\n".format(value['transcript_name'], value['sequence'])
        out_file.write(sequence)
    out_file.close()


