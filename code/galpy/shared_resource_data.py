from galeupy import db_function, logging_utility
import os
from pathlib import PurePosixPath


def common_data_basic(db_config, main_path, log_file):
    logger = logging_utility.logger_function(__name__, log_file)
    logger.info("Common Data will load now prior to parsing your real data...")

    host = db_config.host
    db_username = db_config.db_username
    db_password = db_config.db_password
    db_prefix = db_config.db_prefix

    db_name = db_function.DbNames(db_prefix)
    db_sres = db_function.Database(host, db_username, db_password, db_name.sres, 1)

    upload_shared_data(db_sres, main_path, logger)


def upload_shared_data(db, main_path, logger):
    shared_data = UploadSharedData(main_path, db)

    shared_data.upload_genetic_code(logger)
    shared_data.upload_taxonomy_data(logger)
    shared_data.upload_go_evidence(logger)
    shared_data.upload_go_term(logger)
    shared_data.upload_gram_strain(logger)


class DefaultSharedData:
    def __init__(self, main_path):
        gram_strain_file = 'data/commonData/GramStrain/Data.txt'
        go_term_file = 'data/commonData/Download/go_daily-termdb-tables/term.txt'
        go_evidence_file = 'data/commonData/Download/goevidence.out'
        taxonomy_file = 'data/commonData/Download/taxon.out'
        genetic_code_file = 'data/commonData/Download/gene_code.out'

        self.genetic_code_file = PurePosixPath(main_path, genetic_code_file)
        self.taxonomy_file = PurePosixPath(main_path, taxonomy_file)
        self.go_evidence_file = PurePosixPath(main_path, go_evidence_file)
        self.go_term_file = PurePosixPath(main_path, go_term_file)
        self.gram_strain_file = PurePosixPath(main_path, gram_strain_file)


class UploadSharedData(DefaultSharedData):
    def __init__(self, main_path, db_shared_resource):
        DefaultSharedData.__init__(self, main_path)

        sql_gc = """SELECT * FROM GeneticCode;"""
        sql_tax = """SELECT * FROM Taxon;"""
        sql_go_evidence = """SELECT * FROM GOEvidenceCode;"""
        sql_go_term = """SELECT * FROM GOTerm;"""
        sql_gram_strain = """SELECT * FROM GramStrain;"""

        self.db_shared_resource = db_shared_resource

        self.row_genetic_code = db_shared_resource.rowcount(sql_gc)
        self.row_taxonomy = db_shared_resource.rowcount(sql_tax)
        self.row_go_evidence_code = db_shared_resource.rowcount(sql_go_evidence)
        self.row_go_term = db_shared_resource.rowcount(sql_go_term)
        self.row_gram_strain = db_shared_resource.rowcount(sql_gram_strain)

    def upload_genetic_code(self, logger):
        if self.row_genetic_code == 0:
            logger.debug("Upload shared genetic code data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE GeneticCode FIELDS TERMINATED BY '\t' OPTIONALLY 
                ENCLOSED BY '"' LINES TERMINATED BY '\n'(GENETIC_CODE_ID, NCBI_GENETIC_CODE_ID, ABBREVIATION, NAME,
                CODE, STARTS);""".format(self.genetic_code_file)
            self.db_shared_resource.insert(query)

    def upload_taxonomy_data(self, logger):
        if self.row_taxonomy == 0:
            logger.debug("Upload shared taxonomy data data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE Taxon FIELDS TERMINATED BY '\t' 
                OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' (NCBI_TAXON_ID, PARENT_ID, TAXON_NAME, TAXON_STRAIN,
                RANK, GENETIC_CODE_ID, MITOCHONDRIAL_GENETIC_CODE_ID);""".format(self.taxonomy_file)
            self.db_shared_resource.insert(query)

    def upload_go_evidence(self, logger):
        if self.row_go_evidence_code == 0:
            logger.debug("Upload shared go evidence data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE GOEvidenceCode FIELDS TERMINATED BY '\t' OPTIONALLY
                ENCLOSED BY '"' LINES TERMINATED BY '\n' (NAME, DESCRIPTION, MODIFICATION_DATE);""".format(
                self.go_evidence_file)
            self.db_shared_resource.insert(query)

    def upload_go_term(self, logger):
        if self.row_go_term == 0:
            logger.debug("Upload shared go term data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE GOTerm FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED
                BY '"' LINES TERMINATED BY '\n';""".format(self.go_term_file)
            self.db_shared_resource.insert(query)

    def upload_gram_strain(self, logger):
        if self.gram_strain_file == 0:
            logger.debug("Upload shared gram strain data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE GramStrain FIELDS TERMINATED BY '\t' OPTIONALLY 
                ENCLOSED BY '"' LINES TERMINATED BY '\n'(TAXON_ID, STRAIN_TYPE, ORGANISM, MEMBRANE_TYPE);""".format(
                self.gram_strain_file)
            self.db_shared_resource.insert(query)
