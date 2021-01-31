import os
from .dbconnect import DbNames, Database
import logging
from pathlib import Path, PurePosixPath
import urllib.request
import urllib.error
import tarfile
import re
_logger = logging.getLogger("galpy.commondata")


def common_data_basic(db_config, main_path):
    _logger.info("Common Data will load now prior to parsing your real data...")

    host = db_config.host
    db_username = db_config.db_username
    db_password = db_config.db_password
    db_prefix = db_config.db_prefix

    db_name = DbNames(db_prefix)
    db_sres = Database(host, db_username, db_password, db_name.sres, 1)

    upload_shared_data(db_sres, main_path)


def upload_shared_data(db, main_path):
    shared_data = UploadCommonData(main_path, db)

    shared_data.upload_genetic_code()
    shared_data.upload_taxonomy_data()
    shared_data.upload_go_evidence()
    shared_data.upload_go_term()
    shared_data.upload_gram_strain()


class DefaultSharedData:
    def __init__(self, data_path):
        self.data_path = Path(data_path)

        gram_strain_file = 'GramStrain.txt'
        go_term_file = 'go_daily-termdb-tables/term.txt'
        go_evidence_file = 'goevidence.out'
        taxonomy_file = 'taxon.out'
        genetic_code_file = 'gene_code.out'

        self.genetic_code_file = self.data_path.joinpath(genetic_code_file)
        self.taxonomy_file = self.data_path.joinpath(taxonomy_file)
        self.go_evidence_file = self.data_path.joinpath(go_evidence_file)
        self.go_term_file = self.data_path.joinpath(go_term_file)
        self.gram_strain_file = self.data_path.joinpath(gram_strain_file)


class UploadCommonData(DefaultSharedData):
    def __init__(self, main_path, db_shared_resource):
        DefaultSharedData.__init__(self, main_path)

        sql_gc = """SELECT * FROM GeneticCode;"""
        sql_tax = """SELECT * FROM Taxon;"""
        sql_go_evidence = """SELECT * FROM GOEvidenceCode;"""
        sql_go_term = """SELECT * FROM GOTerm;"""
        sql_gram_strain = """SELECT * FROM GramStrain;"""

        self.db_sres = db_shared_resource

        self.row_genetic_code = self.db_sres.rowcount(sql_gc)
        self.row_taxonomy = self.db_sres.rowcount(sql_tax)
        self.row_go_evidence_code = self.db_sres.rowcount(sql_go_evidence)
        self.row_go_term = self.db_sres.rowcount(sql_go_term)
        self.row_gram_strain = self.db_sres.rowcount(sql_gram_strain)

    def upload_genetic_code(self):
        if self.row_genetic_code == 0:
            _logger.debug("Upload shared genetic code data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE GeneticCode FIELDS TERMINATED BY '\t' OPTIONALLY 
                ENCLOSED BY '"' LINES TERMINATED BY '\n'(GENETIC_CODE_ID, NCBI_GENETIC_CODE_ID, ABBREVIATION, NAME,
                CODE, STARTS);""".format(self.genetic_code_file)
            self.db_sres.insert(query)

    def upload_taxonomy_data(self):
        if self.row_taxonomy == 0:
            _logger.debug("Upload shared taxonomy data data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE Taxon FIELDS TERMINATED BY '\t' 
                OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' (NCBI_TAXON_ID, PARENT_ID, TAXON_NAME, TAXON_STRAIN,
                RANK, GENETIC_CODE_ID, MITOCHONDRIAL_GENETIC_CODE_ID);""".format(self.taxonomy_file)
            self.db_sres.insert(query)

    def upload_go_evidence(self):
        if self.row_go_evidence_code == 0:
            _logger.debug("Upload shared go evidence data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE GOEvidenceCode FIELDS TERMINATED BY '\t' OPTIONALLY
                ENCLOSED BY '"' LINES TERMINATED BY '\n' (NAME, DESCRIPTION, MODIFICATION_DATE);""".format(
                self.go_evidence_file)
            self.db_sres.insert(query)

    def upload_go_term(self):
        if self.row_go_term == 0:
            _logger.debug("Upload shared go term data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE GOTerm FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED
                BY '"' LINES TERMINATED BY '\n';""".format(self.go_term_file)
            self.db_sres.insert(query)

    def upload_gram_strain(self):
        if self.gram_strain_file == 0:
            _logger.debug("Upload shared gram strain data")
            query = """LOAD DATA LOCAL INFILE '{}' INTO TABLE GramStrain FIELDS TERMINATED BY '\t' OPTIONALLY 
                ENCLOSED BY '"' LINES TERMINATED BY '\n'(TAXON_ID, STRAIN_TYPE, ORGANISM, MEMBRANE_TYPE);""".format(
                self.gram_strain_file)
            self.db_sres.insert(query)


class DownloadCommonData:
    def __init__(self, download_path):
        self.download_path = download_path

    def download_file(self, url):

        # head, tail = os.path.split(url)
        url_filename = Path(url).name
        filename = Path(self.download_path).joinpath(url_filename)
        try:
            _logger.info("Starting to download: {}.".format(url))
            _logger.info("Downloading to : {}.".format(filename))
            urllib.request.urlretrieve(url, filename)
        except urllib.error.URLError as e:
            _logger.error("Error in the URL")
        finally:
            _logger.info("Download Complete: {}".format(url))
            return filename

    def unpack_tar(self, filename, out_file=None):
        if out_file is None:
            out_file = self.download_path
        # theTarFile = Path +FileName
        tar_file = filename
        _logger.info("Starting to unpack {}".format(filename))

        tfile = tarfile.open(tar_file)
        if tarfile.is_tarfile(tar_file):
            tfile.extractall(out_file)
        else:
            _logger.info(tar_file + " is not a tarfile.")
        tfile.close()
        _logger.info("Completed unpacking of {}".format(filename))

    def download_goterm_data(self):
        _logger.info("Starting to download go_daily-termdb-tables.tar.gz...............")
        target = "http://archive.geneontology.org/latest-termdb/go_daily-termdb-tables.tar.gz"
        filename = self.download_file(target)
        self.unpack_tar(filename)

    def download_taxon_data(self):
        _logger.info("Starting downloading NCBI taxon data...............")
        target = "ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"
        filename = self.download_file(target)
        taxon_data_path = Path(self.download_path).joinpath("taxdump")
        self.unpack_tar(filename, taxon_data_path)

    def make_taxon(self, genetic_code_id_dct):
        """
        This script combines data from names.dmp and taxon.dmp from
        genbank and makes into our taxonomy table format.
        More info: ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump_readme.txt

        The nodes.dmp file does not have proper mitochondrial code
        so just replacing it with 1 for the time being
        """
        default_download_path = Path(self.download_path).joinpath("taxdump")
        name_file = default_download_path.joinpath("names.dmp")
        nodes_file = default_download_path.joinpath("nodes.dmp")

        taxonomy_file = Path(self.download_path).joinpath("taxon.out")

        fh = open(name_file, 'r')
        names = {}
        for i, line in enumerate(fh):
            line = line.rstrip()
            if re.search(r'scientific name', line):
                tmp = re.split(r'\t+', line)
                names[tmp[0]] = tmp[2]

        write_fh = open(taxonomy_file, "w")
        fh = open(nodes_file, 'r')
        for i, line in enumerate(fh):
            line = line.rstrip()
            tmp = re.split(r'\t\|\t', line)
            genetic_code_id = genetic_code_id_dct[tmp[6]]
            mit_id = genetic_code_id_dct[tmp[8]]
            string1 = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(tmp[0], tmp[1], names[tmp[0]], '', tmp[2], genetic_code_id,
                                                            mit_id)
            write_fh.write(string1)
        return taxonomy_file

    def parse_genetic_code(self, read_file=None, write_file=None):
        """
        Author : Arijit
        Date : 20th Jun 2017
        Description: This script takes genetic code file downloaded from ncbi taxonomy directory
        and parses into sres.GeneticCode table format.
        More Info : ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump_readme.txt
        """
        if read_file is None:
            read_file = Path(self.download_path).joinpath("gencode.dmp")
        if write_file is None:
            write_file = Path(self.download_path).joinpath("gene_code.out")

        read_fh = open(read_file, 'r')
        write_fh = open(write_file, "w")
        id_dct = {}

        for i, line in enumerate(read_fh):
            line = line.rstrip()
            tmp = re.split(r'\t\|\t', line)
            tmp[4] = re.sub(r'\t\|', '', tmp[4])
            id_dct[tmp[0]] = i + 1
            string1 = '{}\t{}\t{}\t{}\t{}\t{}\n'.format(i + 1, tmp[0], tmp[1], tmp[2], tmp[3], tmp[4])
            write_fh.write(string1)

        return id_dct, write_file

    def download_parse_goterm_and_taxon(self):
        self.download_goterm_data()
        self.download_taxon_data()
        go_term_file, id_dct = self.parse_genetic_code()
        taxon_file = self.make_taxon(go_term_file)
        return go_term_file, taxon_file
