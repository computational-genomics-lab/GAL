from __future__ import print_function
import os
import sys
from pathlib import Path
from galeupy.BioFile import genbank_parser, gff_parser, blastparser, protein_algorithm_utility, interproscan_parser
from galeupy import external_program, basic_utility as bu, db_table_utility as db_table, organism_function
from galeupy import post_processing_utility as ppf
from galeupy import data_process_utility as gtp, directory_utility, logging_utility
from galeupy import config_utility
import json


def process_central_dogma_data(config, random_string, id_list, present_dir, log_file):
    db_config = config.db_config
    org_config = config.org_config
    path_config = config.path_config

    data_type = check_data_type(org_config, path_config)
    logger = logging_utility.logger_function(__name__, log_file)
    if data_type == 'type1':
        logger.info('Processing  GenBank type Data...')
        (sequence_dct, feature_dct) = process_type1_data(org_config)  # GenBank Annotation
        process_minimal_annotation_data(db_config, org_config, path_config, sequence_dct, feature_dct, id_list, logger)
        db_table.upload_gal_table_data(db_config, path_config.upload_dir, logger)

    elif data_type == 'type2':  # No Annotation
        logger.info("Processing No Annotation type Data...")
        (sequence_dct, gff_dct) = process_type2_data(org_config, path_config, random_string, present_dir, log_file)
        process_minimal_annotation_data(db_config, org_config, path_config, sequence_dct, gff_dct, id_list, logger)
        db_table.upload_gal_table_data(db_config, path_config.upload_dir, logger)

    elif data_type == "type3":  # Minimal Annotation
        logger.info("Processing Minimal Annotation type Data...")
        (sequence_dct, gff_dct) = process_type3_data(org_config)
        process_minimal_annotation_data(db_config, org_config, path_config, sequence_dct, gff_dct, id_list, logger)
        db_table.upload_gal_table_data(db_config, path_config.upload_dir, logger)

    elif data_type == 'type4':  # Partial Annotation
        logger.info("Processing Complete Annotation type Data...")
        (sequence_dct, gff_dct) = process_type4_data(org_config)
        process_minimal_annotation_data(db_config, org_config, path_config, sequence_dct, gff_dct, id_list, logger)
        db_table.upload_gal_table_data(db_config, path_config.upload_dir, logger)

    return type


def process_minimal_annotation_data(db_config, org_config, path_config, sequence_dct,  gff_dct, id_list, logger):
    #  logger = logging_utility.logger_function(__name__, log_file)
    logger.info("You are in minimal data processing part.")
    taxonomy_id = organism_function.get_taxonomy_id(db_config, org_config.organism)
    org_info = organism_function.OrganismInfo(org_config.organism, taxonomy_id, org_config.version)
    gal_id = DatabaseID(id_list)
    gal_fh = directory_utility.GALFileHandler(path_config.upload_dir)

    present_day = bu.get_date()
    gal_id.increase_by_value(1)
    for scaffold, scaffold_dct in gff_dct.items():
        if scaffold in sequence_dct:
            sequence = sequence_dct[scaffold]
            db_table.na_sequence_imp_scaffold(gal_fh, gal_id.NaSequenceId, scaffold, sequence, org_info, present_day)
            scaffold_na_sequence_id = gal_id.NaSequenceId
            gal_id.NaSequenceId += 1
            for feature, feature_dct in scaffold_dct.items():
                if feature == 'gene':
                    for gene_id, gene_dct in feature_dct.items():
                        gtp.process_gff_gene_data(gal_id, gal_fh, org_info, scaffold, gene_id, gene_dct,
                                                  scaffold_na_sequence_id)
                        gal_id.NaSequenceId += 1
                elif feature == 'repeat_region':
                    gtp.process_repeat_data(gal_id, gal_fh, feature, feature_dct, scaffold_na_sequence_id)


def process_type1_data(org_config):
    """ GenBank annotation type data process """
    print(org_config.GenBank)
    file_handler = genbank_parser.open_input_file(org_config.GenBank)
    (feature_dct, sequence_dct) = genbank_parser.get_data(file_handler)

    feature_dct = ppf.fix_multiple_splicing_bugs(feature_dct)

    model_gff_dct = ppf.create_gal_model_dct(sequence_dct, feature_dct)
    return sequence_dct, model_gff_dct


def process_type2_data(org_config, path_config, random_name, gal_dir, log_file):
    """
        No Annotation type data
        Only fasta file is provided
        This type of data reference genome name
    """
    logger = logging_utility.logger_function(__name__, log_file)
    sequence_file = org_config.fasta
    reference_genome = org_config.RefOrg
    upload_dir = path_config.upload_dir
    file_name = os.path.join(upload_dir, random_name)
    gff_file_name = file_name + ".gff"
    program_name = org_config.program

    if program_name:
        if program_name.lower() == 'augustus':
            program = path_config.augustus
            external_program.run_augustus(program, reference_genome, sequence_file, gff_file_name, logger)
            external_program.fetch_protein(gal_dir, gff_file_name)
        elif program_name.lower() == 'genemark':
            program = path_config.genmark
            model_file_dir = path_config.genmark_model
            external_program.run_genemark(program, model_file_dir, reference_genome, sequence_file, file_name, logger)
        else:
            logger.error('Please check the gene prediction program name')
            sys.exit(0)
    else:
        program = path_config.augustus
        external_program.run_augustus(program, reference_genome, sequence_file, gff_file_name, logger)
        external_program.fetch_protein(gal_dir, gff_file_name)

    protein_file_name = os.path.join(path_config.upload_dir, random_name + ".aa")
    blast_file_name = os.path.join(path_config.upload_dir, random_name + ".blast")
    blast_program = path_config.blastp
    external_program.run_blast(blast_program, protein_file_name, blast_file_name, gal_dir, logger)

    sequence_dct = bu.read_fasta_to_dictionary(org_config.fasta)
    # gff_dct = gff_parser.read_gff3_augustus(gff_file_name)
    gff_dct = gff_parser.read_gff3_genbank(gff_file_name)
    blast_dct = blastparser.parse_file(blast_file_name)

    model_gff_dct = ppf.create_gal_model_dct(sequence_dct, gff_dct, blast_dct)

    return sequence_dct, model_gff_dct


def process_type3_data(org_config):
    """
        Fasta and gff file is provided
    """

    sequence_dct = bu.read_fasta_to_dictionary(org_config.fasta)

    gff_dct = gff_parser.read_gff3_genbank(org_config.gff)

    model_gff_dct = ppf.create_gal_model_dct(sequence_dct, gff_dct)
    return sequence_dct, model_gff_dct


def process_type4_data(org_config):
    """ Partial Annotation type data process"""
    sequence_dct = bu.read_fasta_to_dictionary(org_config.fasta)
    gff_dct = gff_parser.read_gff3_genbank(org_config.gff)
    blast_dct = bu.product_to_dictionary(org_config.product)
    model_gff_dct = ppf.create_gal_model_dct(sequence_dct, gff_dct, blast_dct)

    return sequence_dct, model_gff_dct


def process_protein_feature_algorithm_data(config, random_str, taxonomy_dct, log_file):
    logger = logging_utility.logger_function(__name__, log_file)

    db_config = config.db_config
    org_config = config.org_config
    path_config = config.path_config

    protein_path = os.path.join(path_config.upload_dir, random_str + '.aa')
    taxonomy_id = taxonomy_dct['TAXON_ID']
    organism_function.create_protein_file(db_config, taxonomy_id, org_config.version, protein_path)
    protein_feature_path = directory_utility.ProteinFeatureFileName(path_config.upload_dir, random_str)

    organism_type = organism_function.find_organism_type(org_config.organism, taxonomy_dct, db_config)

    hmmpfam_program = path_config.HMMSCAN
    pfam_db = path_config.hmm_db
    logger.info('External Program: HMMPFAM started')
    external_program.run_hmmpfam(hmmpfam_program, pfam_db, protein_path, protein_feature_path.PFam_out, logger)
    logger.info('HMMpFAM result: {}'.format(protein_feature_path.PFam_out))

    signalp_program = path_config.signalp
    logger.info('External Program: SignalP started')
    external_program.run_signal_p(signalp_program, protein_path, protein_feature_path.SignalP_out, logger, organism_type)
    logger.info('Signalp result: {}'.format(protein_feature_path.SignalP_out))

    tmhmm_path = path_config.TMHMM
    logger.info('External Program: TMHMM started')
    external_program.run_tmhmm(tmhmm_path, protein_path, protein_feature_path.TmHmm_out, logger)
    logger.info('TMHMM result: {}'.format(protein_feature_path.TmHmm_out))

    protein_feature_id_list = db_table.get_protein_feature_table_status(db_config)

    protein_algorithm_utility.parse_hmmscan_result(protein_feature_path.PFam_out, protein_feature_path.PFam,
                                                   protein_feature_id_list)

    protein_algorithm_utility.process_signalp_result(protein_feature_path.SignalP_out, protein_feature_path.SignalP,
                                                     protein_feature_id_list )
    protein_algorithm_utility.process_tmhmm_result(protein_feature_path.TmHmm_out, protein_feature_path.TmHmm,
                                                   protein_feature_id_list)

    db_table.upload_protein_feature_table_data(db_config, protein_feature_path)


def process_interpro_data(db_config, org_config, path_config, taxonomy_id, log_file):
    logger = logging_utility.logger_function(__name__, log_file)

    if os.path.exists(org_config.interproscan):
        logger.info('processing Interproscan data')
        interproscan_parser.process_interpro_data(db_config, path_config.upload_dir, org_config.interproscan,
                                                  taxonomy_id, org_config.version)


def check_data_type(org_config, path_config):
    type1 = "type1"  # "GenBank"
    type2 = "type2"  # "No Annotation"
    type3 = "type3"  # "Minimal Annotation"
    type4 = "type4"  # "Complete Annotation"

    genbank = org_config.GenBank
    fasta = org_config.fasta
    gff = org_config.gff
    product = org_config.product
    ref_org = org_config.RefOrg
    upload_dir = path_config.upload_dir

    if genbank != '':
        return type1
    else:
        if fasta != "" and gff == "" and product == "":
            if ref_org != "" and upload_dir != "":
                return type2
            elif ref_org == "":
                print("\t\tError: Reference Genome File does not exist\n")
            elif upload_dir == "":
                print("\t\tError: Upload path is empty\n")
        elif fasta != "" and gff != "" and product == "":
            return type3
        elif fasta != "" and gff != "" and product != "":
            return type4


class DatabaseID:
    def __init__(self, id_list):
        self.NaSequenceId = id_list[0]
        self.NaFeatureId = id_list[1]
        self.na_location_Id = id_list[2]
        self.GeneInstanceId = id_list[3]
        self.ProteinId = id_list[4]

    def increase_by_value(self, value):
        self.NaSequenceId += value
        self.NaFeatureId += value
        self.na_location_Id += value
        self.GeneInstanceId += value
        self.ProteinId += value


def file_existence_check(filename):
    if not os.path.isfile(filename):
        print("\t\tError:: %s file Does not exist ....." % filename)
        return 0
    else:
        return 1

'''
def config_file_handler_old(db_config_file, path_config_file, org_config_file):
    if os.path.isfile(db_config_file):
        db_config = config_utility.DatabaseConf(db_config_file)
    else:
        print("\t\t\n Database configuration file missing: {}".format(db_config_file))
        sys.exit()

    if os.path.isfile(path_config_file):
        path_config = config_utility.PathConf(path_config_file)
    else:
        print("\t\t\n Path configuration file missing: {}".format(path_config_file))
        sys.exit()

    if os.path.isfile(org_config_file):
        org_config = config_utility.OrganismConf(org_config_file)
    else:
        print("\t\t\n Organism configuration file missing: {}".format(org_config_file))
        sys.exit()

    return db_config, path_config, org_config
'''


class ConfigFileHandler:
    def __init__(self, db_config_file, path_config_file, org_config_file, logger):
        db_config_file = Path(db_config_file)
        path_config_file = Path(path_config_file)
        org_config_file = Path(org_config_file)

        if db_config_file.exists():
            self.db_config = config_utility.DatabaseConf(db_config_file)
        else:
            logger.error("FileNotFoundError: {}".format(db_config_file))
            raise FileNotFoundError

        if path_config_file.exists():
            self.path_config = config_utility.PathConf(path_config_file)
        else:
            logger.error("FileNotFoundError: {}".format(path_config_file))
            raise FileNotFoundError

        if org_config_file.exists():
            self.org_config = config_utility.OrganismConf(org_config_file)
        else:
            logger.error("FileNotFoundError: {}".format(org_config_file))
            raise FileNotFoundError
