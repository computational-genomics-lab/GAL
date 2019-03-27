import configparser


def database_config_reader(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    # config function
    def config_section_map(section):
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    # DebugPrint("skip: %s" % option)
                    print("skip: %s" % option)
            except (RuntimeError, TypeError, NameError, ValueError, AttributeError):
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    host = config_section_map("dbconnection")['host']
    db_username = config_section_map("dbconnection")['db_username']
    db_password = config_section_map("dbconnection")['db_password']
    db_prefix = config_section_map("dbconnection")['database_prefix']

    return host, db_username, db_password, db_prefix


class DatabaseConf:
    def __init__(self, filename):
        (self.host, self.db_username, self.db_password, self.db_prefix) = database_config_reader(filename)


def organism_config_reader(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    # config function
    def config_section_map(section):
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    # DebugPrint("skip: %s" % option)
                    print("skip: %s" % option)
            except (RuntimeError, TypeError, NameError, ValueError, AttributeError):
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    # header : OrganismDetails
    organism = config_section_map('OrganismDetails')['organism']
    version = config_section_map('OrganismDetails')['version']
    source_url = config_section_map('OrganismDetails')['source_url']

    # header : SequenceType
    sequence_type = config_section_map('SequenceType')['sequencetype']

    # header :AnnotationInfo
    if_blastp = config_section_map('AnnotationInfo')['blastp']
    if_signalp = config_section_map('AnnotationInfo')['signalp']
    if_pfam = config_section_map('AnnotationInfo')['pfam']
    if_tmhmm = config_section_map('AnnotationInfo')['tmhmm']

    # header : FilePath
    genbank = config_section_map('filePath')['genbank']
    fasta = config_section_map('filePath')['fasta']
    gff = config_section_map('filePath')['gff']
    product = config_section_map('filePath')['product']
    lastz = config_section_map('filePath')['lastz']
    signalp = config_section_map('filePath')['signalp']
    pfam = config_section_map('filePath')['pfam']
    tmhmm = config_section_map('filePath')['tmhmm']
    interproscan = config_section_map('filePath')['interproscan']

    # header : Other
    program = config_section_map('other')['program']
    ref_org = config_section_map('other')['referencegenome']

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
    config = configparser.ConfigParser()
    config.read(filename)

    # config function
    def config_section_map(section):
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    # DebugPrint("skip: %s" % option)
                    print("skip: %s" % option)
            except (RuntimeError, TypeError, NameError, ValueError, AttributeError):
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    # header : general
    upload_path = config_section_map('general')['upload_path']

    # header : External_Program
    lastz = config_section_map('External_Program')['lastz']
    db_creator = config_section_map('External_Program')['db_creator']
    augustus = config_section_map('External_Program')['augustus']
    genmark = config_section_map('External_Program')['genmark']
    signalp = config_section_map('External_Program')['signalp']
    tmhmm = config_section_map('External_Program')['tmhmm']
    hmmscan = config_section_map('External_Program')['hmmscan']
    blastp = config_section_map('External_Program')['blastp']

    # header : Associated_External_Program_Path
    blast_path = config_section_map('Associated_External_Program_Path')['blast']
    hmm_db = config_section_map('Associated_External_Program_Path')['hmm_db']
    genmark_model = config_section_map('Associated_External_Program_Path')['genmark_model']
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
