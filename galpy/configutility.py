import configparser
from pathlib import Path
import logging
_logger = logging.getLogger("galpy.configutility")


class ConfigFileHandler:
    def __init__(self, db_config_file, path_config_file, org_config_file):
        """
        Reads ini configuration files for GAL
        parameters
        -----------
        db_config_file: str
            file path for database configuration file
        path_config_file: str
            file path for path configuration file
        org_config_file: str
            file path for organism configuration file
        """

        self.db_config_file = Path(db_config_file)
        self.path_config_file = Path(path_config_file)
        self.org_config_file = Path(org_config_file)

        _logger.info(f"DB configuration file: {self.db_config_file}")
        _logger.info(f"Path configuration file: {self.path_config_file}")
        _logger.info(f"Organism configuration file: {self.org_config_file}")

    @property
    def db_config(self):
        if self.path_check(self.db_config_file):
            db_config = DatabaseConf(self.db_config_file)
            return db_config

    @property
    def path_config(self):
        if self.path_check(self.path_config_file):
            path_config = PathConf(self.path_config_file)
            return path_config

    @property
    def org_config(self):
        if self.path_check(self.org_config_file):
            org_config = OrganismConf(self.org_config_file)
            return org_config

    @staticmethod
    def path_check(file_path):
        if file_path.exists():
            return file_path
        else:
            _logger.error(f"FileNotFoundError: {file_path}")
            raise FileNotFoundError


class ConfigReader:
    def __init__(self, filename):
        """
        Reads an ini configuration file
        parameters
        ------------
        filename: str
            path for the ini configuration file
        """
        self.config_file = Path(filename)

    @property
    def config(self):
        """
        Returns the configparser object

        Returns
        --------
        config: configparser object
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config

    def section_map(self, section):
        """
        Return a section dict
        parameters
        ------------
        section: str
            name of section

        returns
        --------
        dict1: dict
            dictionary for the section name
        """
        dict1 = {}
        if self.config.has_section(section):
            options = self.config.options(section)
            for option in options:
                try:
                    dict1[option] = self.config.get(section, option)
                    if dict1[option] == -1:
                        # DebugPrint("skip: %s" % option)
                        _logger.error("skip: %s" % option)
                except (RuntimeError, TypeError, NameError, ValueError, AttributeError):
                    _logger.error("exception on %s!" % option)
                    dict1[option] = None
        return dict1

    def check_key(self, section_dct, key):
        key_entry = section_dct[key] if key in section_dct else None
        if key_entry == '' or key_entry is None:
            return None
        # to solve the path
        if not Path(key_entry).is_absolute():
            key_entry = self.config_file.parent.resolve().joinpath(key_entry)
        return key_entry


def database_config_reader(filename):
    config_obj = ConfigReader(filename)

    section_map = config_obj.section_map("dbconnection")
    host = section_map['host']
    db_username = section_map['db_username']
    db_password = section_map['db_password']
    db_prefix = section_map['database_prefix']

    db_port = section_map['port'] if 'port' in section_map else None
    if db_port == '':
        db_port = None
    if db_port is not None:
        db_port = int(db_port)
    return host, db_username, db_password, db_prefix, db_port


class DatabaseConf:
    def __init__(self, filename):
        (self.host, self.db_username, self.db_password, self.db_prefix, self.db_port) = database_config_reader(filename)


def organism_config_reader(filename):
    config_obj = ConfigReader(filename)

    # header : OrganismDetails
    config_org_details = config_obj.section_map('OrganismDetails')
    organism = config_org_details['organism']
    version = config_org_details['version']
    source_url = config_org_details['source_url']

    # header : SequenceType
    sequence_type = config_obj.section_map('SequenceType')['sequencetype']

    # header :AnnotationInfo
    config_org_annotation = config_obj.section_map('AnnotationInfo')
    if_blastp = config_org_annotation['blastp'] if 'blastp' in config_org_annotation else None
    if_signalp = config_org_annotation['signalp'] if 'signalp' in config_org_annotation else None
    if_pfam = config_org_annotation['pfam'] if 'pfam' in config_org_annotation else None
    if_tmhmm = config_org_annotation['tmhmm'] if 'tmhmm' in config_org_annotation else None

    # header : FilePath
    config_annotation_path = config_obj.section_map('filePath')
    genbank = config_obj.check_key(config_annotation_path, 'genbank')
    fasta = config_obj.check_key(config_annotation_path, 'fasta')
    gff = config_obj.check_key(config_annotation_path, 'gff')
    product = config_obj.check_key(config_annotation_path, 'product')

    lastz = config_obj.check_key(config_annotation_path, 'lastz')
    signalp = config_obj.check_key(config_annotation_path, 'signalp')
    pfam = config_obj.check_key(config_annotation_path, 'pfam')
    tmhmm = config_obj.check_key(config_annotation_path, 'tmhmm')
    interproscan = config_obj.check_key(config_annotation_path, 'interproscan')

    # header : Other
    config_other = config_obj.section_map('other')
    program = config_obj.check_key(config_other, 'program')
    ref_org = config_obj.check_key(config_other, 'referencegenome')

    organism_config_dct = {
        'organism': organism,
        'orgVersion': version,
        'source_url': source_url,
        'sequence_type': sequence_type,
        'ifblastp': if_blastp,
        'ifsignalp': if_signalp,
        'ifpfam': if_pfam,
        'iftmhmm': if_tmhmm,
        'GenBank': genbank,
        'fasta': fasta,
        'gff': gff,
        'product': product,
        'lastz': lastz,
        'signalp': signalp,
        'pfam': pfam,
        'tmhmm': tmhmm,
        'interproscan': interproscan,
        'program': program,
        'RefOrg': ref_org
    }

    return organism_config_dct


class OrganismConf:
    def __init__(self, filename):
        organism_config_dct = organism_config_reader(filename)
        self.org_config_file = Path(filename)
        self.organism = organism_config_dct['organism']
        self.version = organism_config_dct['orgVersion']

        self.is_blastp = organism_config_dct['ifblastp']
        self.is_signalp = organism_config_dct['ifsignalp']
        self.is_pfam = organism_config_dct['ifpfam']
        self.is_tmhmm = organism_config_dct['iftmhmm']

        self.GenBank = organism_config_dct['GenBank']
        self.fasta = organism_config_dct['fasta']
        self.gff = organism_config_dct['gff']
        self.product = organism_config_dct['product']
        self.lastz = organism_config_dct['lastz']
        self.signalp = organism_config_dct['signalp']
        self.pfam = organism_config_dct['pfam']
        self.tmhmm = organism_config_dct['tmhmm']
        self.interproscan = organism_config_dct['interproscan']

        self.program = organism_config_dct['program']
        self.RefOrg = organism_config_dct['RefOrg']


def path_config_reader(filename):
    config_obj = ConfigReader(filename)

    # header : general
    general_section = config_obj.section_map("general")
    upload_path = general_section['upload_path'] if 'upload_path' in general_section else None

    # header : External_Program
    external_program_section = config_obj.section_map("External_Program")

    lastz = external_program_section['lastz'] if 'lastz' in external_program_section else None
    db_creator = external_program_section['db_creator'] if 'db_creator' in external_program_section else None
    augustus = external_program_section['augustus'] if 'augustus' in external_program_section else None
    genmark = external_program_section['genmark'] if 'genmark' in external_program_section else None
    signalp = external_program_section['signalp'] if 'signalp' in external_program_section else None
    tmhmm = external_program_section['tmhmm'] if 'tmhmm' in external_program_section else None
    hmmscan = external_program_section['hmmscan'] if 'hmmscan' in external_program_section else None
    blastp = external_program_section['blastp'] if 'blastp' in external_program_section else None

    # header : Associated_External_Program_Path
    associated_ext_program_section = config_obj.section_map("Associated_External_Program_Path")
    blast_path = associated_ext_program_section['blast'] if 'blast' in associated_ext_program_section else None
    hmm_db = associated_ext_program_section['hmm_db'] if 'hmm_db' in associated_ext_program_section else None
    genmark_model = associated_ext_program_section['genmark_model'] if 'genmark_model' in associated_ext_program_section else None
    # header:

    path_config_dct = {
        'upload_path': upload_path,
        'lastz': lastz,
        'db_creator': db_creator,
        'augustus': augustus,
        'genmark': genmark,
        'signalp': signalp,
        'TMHMM': tmhmm,
        'HMMSCAN': hmmscan,
        'blastp': blastp,
        'blast_path': blast_path,
        'hmm_db': hmm_db,
        'genmark_model': genmark_model
    }

    return path_config_dct


class PathConf:
    def __init__(self, filename):
        path_config_dct = path_config_reader(filename)

        self.upload_dir = path_config_dct['upload_path']
        self.lastz = path_config_dct['lastz']
        self.db_creator = path_config_dct['db_creator']
        self.augustus = path_config_dct['augustus']
        self.genmark = path_config_dct['genmark']
        self.signalp = path_config_dct['signalp']
        self.TMHMM = path_config_dct['TMHMM']
        self.HMMSCAN = path_config_dct['HMMSCAN']
        self.blastp = path_config_dct['blastp']

        self.blast_path = path_config_dct['blast_path']
        self.hmm_db = path_config_dct['hmm_db']
        self.genmark_model = path_config_dct['genmark_model']


def config_string_generator( org_name, org_version, reg_org, genbank, fasta, gff, product):
    organism_part = """
[OrganismDetails]

Organism: {}
version: {}
source_url:
    """.format(org_name, org_version)

    other_part = """
[SequenceType]
SequenceType: chromosome

[AnnotationInfo]
blastp: yes
signalp: yes
pfam: yes
tmhmm: yes

[filePath]
GenBank: {}
FASTA:{}
GFF:{}
LastZ:
SignalP:
pfam:
TMHMM:
Product:{}
interproscan:

[other]
program:
ReferenceGenome:{}
    """ .format(genbank, fasta, gff, product, reg_org)

    full_config = '{}\n{}'.format(organism_part, other_part)
    return full_config
