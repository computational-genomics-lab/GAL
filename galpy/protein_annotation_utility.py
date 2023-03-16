import logging
from pathlib import Path
from .dbtable_utility import TableStatusID
import re
from .BioFile.interproscan_parser import ParseInterproResult
from .directory_utility import ProteinAnnotationFiles

_logger = logging.getLogger("galpy.protein_annotation_utility")


class TranscriptMap:
    def __init__(self, db_dots, taxonomy_id, org_version):
        self.db_dots = db_dots
        self.taxonomy_id = taxonomy_id
        self.org_version = org_version

    @property
    def transcript_map_dct(self):
        sql_query = f"""select p.name as 'name1',naf.name as 'name2', gi.gene_instance_id from 
    Protein p, GeneInstance gi, NAFeatureImp naf, NASequenceImp na where 
    gi.gene_instance_id = p.gene_instance_id and
    naf.na_feature_id = gi.na_feature_id and
    naf.feature_type='mRNA' and
    na.na_sequence_id = naf.na_sequence_id and 
    na.taxon_id = {self.taxonomy_id} and
    na.sequence_version = {self.org_version}"""

        transcript_name_dct = {}

        result = self.db_dots.query(sql_query)
        for i, value in enumerate(result):
            name1 = value['name1']
            name2 = value['name2']
            gene_instance_id = value['gene_instance_id']

            modified_gene_name = self.modify_transcript_name(name1)
            transcript_name_dct[modified_gene_name] = gene_instance_id
            transcript_name_dct[name2] = gene_instance_id

        return transcript_name_dct

    @staticmethod
    def modify_transcript_name(gene_name):
        modified_transcript_name = ''
        match_obj = re.search(r'\S+_(\S+)', gene_name, re.M | re.I)
        if match_obj:
            modified_transcript_name = match_obj.group(1)

        transcript_prefix = '.t1'
        modified_transcript_name = f'{modified_transcript_name}{transcript_prefix}'

        return modified_transcript_name

    def find_transcript_entry(self, transcript_name):
        protein_instance_id = None
        if transcript_name in self.transcript_map_dct:
            protein_instance_id = self.transcript_map_dct[transcript_name]
        else:
            _logger.error(f'{transcript_name} name is not matching with the database entry')
        return protein_instance_id


class BaseProteinAnnotations(ProteinAnnotationFiles, TableStatusID):
    def __init__(self, db_dots, path_config, org_config, random_str):
        ProteinAnnotationFiles.__init__(self, path_config.upload_dir, random_str)
        TableStatusID.__init__(self, db_dots)
        self.db_dots = db_dots
        self.org_config = org_config
        self.path_config = path_config
        self.random_str = random_str

    @property
    def protein_file(self):
        protein_path = Path(self.path_config.upload_dir).joinpath(self.random_str + '.aa')
        _logger.debug(f"protein_path: {protein_path}")
        return protein_path

    def create_protein_file(self, taxonomy_id, org_version):
        _logger.debug("Creating protein file to store the protein information")

        query = f"""select nf.feature_type, nf.name, p.description, p.gene_instance_id, p.sequence from 
        NASequenceImp ns, NAFeatureImp nf, GeneInstance gi, Protein p where ns.taxon_id = {taxonomy_id}
        and ns.sequence_version = {org_version} and ns.sequence_type_id = 6 and nf.na_sequence_id = ns.na_sequence_id
        and nf.feature_type = 'mRNA' and gi.na_feature_id = nf.na_feature_id  and  
        p.gene_instance_id = gi.gene_instance_id"""

        result = self.db_dots.query(query)
        with open(self.protein_file, 'w') as fh:
            for i, value in enumerate(result):
                header_text = f">{value['name']};gi='{value['gene_instance_id']}'\n{value['sequence']}\n"
                fh.write(header_text)

    @property
    def table_status_dct(self):
        table_info_dct = self.get_protein_feature_table_status()
        return table_info_dct


class ProteinAnnotations(BaseProteinAnnotations, TranscriptMap):
    def __init__(self, db_dots, path_config, org_config, random_str, taxonomy_id, org_version):
        BaseProteinAnnotations.__init__(self, db_dots, path_config, org_config, random_str)
        TranscriptMap.__init__(self, db_dots, taxonomy_id, org_version)
        # self.table_status_dct = self.get_tables_max_id()

    def parse_interproscan_data(self, interpro_file):
        pif_id = self.table_status_dct['interproscan']
        parsed_file_name = Path(self.path_config.upload_dir).joinpath('parsed_interpro_file')

        interpro_obj = ParseInterproResult(interpro_file, parsed_file_name, self.transcript_map_dct)
        interpro_obj.create_parsed_output(pif_id)

        self.upload_interpro_data(parsed_file_name)

    def upload_interpro_data(self, interpro_data):
        _logger.debug("Uploading InterProScan data")
        # For ProteinInstanceFeature table
        sql_1 = f"""LOAD DATA LOCAL INFILE '{interpro_data}' INTO TABLE InterProScan 
        FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';"""
        self.db_dots.insert(sql_1)

    def parse_hmmscan_result(self, parsed_file, upload_file):
        fh = open(parsed_file, 'r')
        pfam_write_fh = open(upload_file, 'w')
        hmm_row_id = self.table_status_dct['tmhmm']

        for i, line in enumerate(fh):
            line = line.rstrip()
            if not line.startswith("#"):
                line_list = line.split()
                list_len = len(line_list)
                if list_len > 19:
                    line_list[18:list_len] = [' '.join(line_list[18:list_len])]
                list_len = len(line_list)
                if list_len == 19:
                    hmm_string = self.process_hmm_scan_single_line(line_list)
                    hmm_row_id += 1
                    hmm_string1 = '{}\t{}\n'.format(hmm_row_id, hmm_string)
                    pfam_write_fh.write(hmm_string1)

    @staticmethod
    def process_hmm_scan_single_line(line_list):
        domain_name = line_list[0]
        accession_id = line_list[1]
        gi_id = line_list[2]
        e_value = line_list[7]
        score = line_list[8]
        bias = line_list[9]
        domain_des = line_list[18]
        match_obj = re.search(r"gi='(.*)'", gi_id, re.M | re.I)
        if match_obj:
            gi_id = match_obj.group(1)
            hmm_string = '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(gi_id, e_value, score, bias, accession_id, domain_name,
                                                             domain_des)
            return hmm_string

    def upload_hmmpfam_data(self, hmmpfam_data):
        # For HmmPfam table
        sql_1 = f"""LOAD DATA LOCAL INFILE '{hmmpfam_data}' INTO TABLE HmmPfam FIELDS TERMINATED BY '\t' OPTIONALLY
                   ENCLOSED BY '"' LINES TERMINATED BY '\n' (`PFAM_ID`, `GENE_INSTANCE_ID`, 
                   `E_VALUE`, `SCORE`, `BIAS`, `ACCESSION_ID`, `DOMAIN_NAME`, `DOMAIN_DESCRIPTION`)"""
        self.db_dots.insert(sql_1)

    def parse_signalp_result(self, parsed_file):
        _logger.debug(f"Reading SignalP file from {parsed_file}")
        fh = open(parsed_file, 'r')
        signalp_write_fh = open(self.SignalP, 'w')
        signalp_row_id = self.table_status_dct['signalp']

        for i, line in enumerate(fh):
            line = line.rstrip()
            if not line.startswith("#"):
                line_list = line.split()
                list_len = len(line_list)

                # if list_len == 12:
                # print(list_len)
                if list_len >= 10:
                    gi_id = get_gi_id(line_list[0])
                    gene_name = gi_id

                    protein_instance_id = self.find_transcript_entry(gene_name)
                    if protein_instance_id is None:
                        continue

                    y_score = line_list[3]
                    y_pos = line_list[4]
                    d_score = line_list[8]
                    status = line_list[9]
                    s_string = f'{protein_instance_id}\t{y_score}\t{y_pos}\t{d_score}\t{status}'
                    signalp_row_id += 1
                    s_string1 = '{}\t{}\n'.format(signalp_row_id, s_string)
                    signalp_write_fh.write(s_string1)

        signalp_write_fh.close()
        fh.close()

    def upload_signalp_data(self):
        _logger.debug(f"Uploading SignalP data from {self.SignalP}")
        # SignalP table
        query = f"""LOAD DATA LOCAL INFILE '{self.SignalP}' INTO TABLE SignalP 
                FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n'"""
        # _logger.debug(query)
        self.db_dots.insert(query)

    def parse_tmhmm_result(self, parsed_file):
        fh = open(parsed_file, 'r')
        tmhmm_write_fh = open(self.TmHmm, 'w')
        tmhmm_row_id = self.table_status_dct['tmhmm']
        for i, line in enumerate(fh):
            line = line.rstrip()
            if not line.startswith("#"):
                line_list = line.split()
                list_len = len(line_list)
                if list_len == 5:
                    if line_list[2] == 'TMhelix':
                        gi_id = get_gi_id(line_list[0])
                        gene_name = gi_id
                        protein_instance_id = self.find_transcript_entry(gene_name)
                        if protein_instance_id is None:
                            continue

                        helix_position = '{}-{}'.format(line_list[3], line_list[4])
                        tmhmm_row_id += 1
                        string1 = '{}\t{}\t\t\t{}\n'.format(tmhmm_row_id, protein_instance_id, helix_position)
                        tmhmm_write_fh.write(string1)
        tmhmm_write_fh.close()
        fh.close()

    def upload_tmhmm_data(self):
        _logger.debug(f"Uploading tmhmm data from {self.TmHmm}")
        # For Tmhmm table
        query = f"""LOAD DATA LOCAL INFILE '{self.TmHmm}' INTO TABLE Tmhmm FIELDS TERMINATED BY '\t' OPTIONALLY
                       ENCLOSED BY '"' LINES 
                       TERMINATED BY '\n' (`TMHMM_ID`, `GENE_INSTANCE_ID`, `INSIDE`, `OUTSIDE`, `TMHELIX`)"""
        # _logger.debug(query)
        self.db_dots.insert(query)


def get_gi_id(string):
    match_obj = re.search(r"gi='(.*)'", string, re.M | re.I)
    if match_obj:
        gi_id = match_obj.group(1)
        return gi_id
    else:
        return string

