import re
from galeupy import db_function, logging_utility


def create_db_connection(db_config):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_dots = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.dots, 0)
    return db_dots


def create_db_connection_shared_resource(db_config):
    db_name = db_function.DbNames(db_config.db_prefix)
    db_sres = db_function.Database(db_config.host, db_config.db_username, db_config.db_password, db_name.sres, 0)
    return db_sres


def update_organism_table(db_config, org_name, org_ver, log_file):
    """
    NEED THE BELLOW INFORMATION FROM ONE SPECIES
        1. genus
        2. order
        3. phylum
        4. class
        5. subclass
        6. family
        7. superkingdom
    """
    logger = logging_utility.logger_function(__name__, log_file)
    taxonomy_dct = get_org_hierarchy(db_config, org_name)
    taxonomy_dct = NoneDict(taxonomy_dct)

    strain = ''
    org = re.split(r'\s', org_name)
    org_size = len(org)
    species = org[0] + " " + org[1]
    if org_size > 2:
        strain_list = org[2:]
        strain = " ".join(strain_list)
    # for x in range(2, org_size):
    #    strain += org[x]

    db_dots = create_db_connection(db_config)

    taxonomy_id = taxonomy_dct['TAXON_ID']
    genus = taxonomy_dct['genus']
    order = taxonomy_dct['order']
    phylum = taxonomy_dct['phylum']
    class_name = taxonomy_dct['class']
    # subclass = taxonomy_dct['subclass']
    family = taxonomy_dct['family']
    super_kingdom = taxonomy_dct['superkingdom']

    query = """
            INSERT INTO Organism(TAXON_ID, SPECIES, STRAIN, PHYLUM, FAMILY, GENUS, ORDERS, CLASS, SUPERKINGDOM, VERSION)
            VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
            """ % (taxonomy_id, species, strain, phylum, family, genus, order, class_name, super_kingdom, org_ver)
    db_dots.insert(query)
    logger.info(" Organism Table update complete")
    return taxonomy_dct


def get_org_hierarchy(db_config, org_name):
    db_sres = create_db_connection_shared_resource(db_config)

    taxonomy_dct = {}
    query = "SELECT NCBI_TAXON_ID, PARENT_ID, TAXON_NAME, TAXON_STRAIN, RANK  FROM Taxon where TAXON_NAME = '%s'"\
            % org_name
    result = db_sres.query(query)
    for i, value in enumerate(result):
        if value['RANK'] == "species" or value['RANK'] == "subspecies":
            taxonomy_dct['TAXON_ID'] = value['NCBI_TAXON_ID']
            taxonomy_id, parent_id, name, rank = get_child_organism_info(db_sres, value['PARENT_ID'])
            taxonomy_dct[rank] = name
            while taxonomy_id != parent_id:
                taxonomy_id, parent_id, name, rank = get_child_organism_info(db_sres, parent_id)
                taxonomy_dct[rank] = name
        elif value['RANK'] == 'no rank':
            taxonomy_id, parent_id, name, rank = get_child_organism_info(db_sres, value['PARENT_ID'])
            if rank == 'species':
                taxonomy_dct['TAXON_ID'] = value['NCBI_TAXON_ID']
                taxonomy_dct[rank] = name
                while taxonomy_id != parent_id:
                    taxonomy_id, parent_id, name, rank = get_child_organism_info(db_sres, parent_id)
                    taxonomy_dct[rank] = name
            else:
                print("Please check the organism name")
        elif value['RANK'] != '':
            print("Please check the organism name")

    return taxonomy_dct


def get_child_organism_info(db, taxonomy_id):
    child_query = "SELECT NCBI_TAXON_ID, PARENT_ID, TAXON_NAME, TAXON_STRAIN, RANK  FROM Taxon WHERE " \
                  "NCBI_TAXON_ID = %d" % taxonomy_id
    result = db.query(child_query)
    for i, value in enumerate(result):
            return value['NCBI_TAXON_ID'], value['PARENT_ID'], value['TAXON_NAME'], value['RANK']


def check_organism_existence(db_config, org_name, org_ver, log_file):
    logger = logging_utility.logger_function(__name__, log_file)

    if not org_name:
        logger.info("Error: Organism Name does not exist \n")
        return True
    else:
        logger.info('Organism: {} version: {}'.format(org_name, org_ver))
        taxonomy_id = get_taxonomy_id(db_config, org_name)
        if taxonomy_id:
            db_dots = create_db_connection(db_config)
            sql_query = "select * from Organism where TAXON_ID = %s and VERSION = %s" % (taxonomy_id, org_ver)
            row_count = db_dots.rowcount(sql_query)
            if row_count == 1:
                logger.info("Error: Organism Name and same version already exists \n")
                return True
            else:
                logger.info("New Organism")
                return False
        else:
            logger.info("Error: Please check the organism name")
            return True


def get_taxonomy_id(db_config, org_name):
    db_sres = create_db_connection_shared_resource(db_config)
    sql_query = "SELECT NCBI_TAXON_ID FROM Taxon where TAXON_NAME = '%s'" % org_name
    data = db_sres.query_one(sql_query)
    if data is not None:
        taxonomy_id = data['NCBI_TAXON_ID']
        if taxonomy_id is None:
            print("Error :Organism Name has issue:")
        return taxonomy_id


def organism_count(db_config):
    db_dots = create_db_connection(db_config)
    sql_query = "SELECT * FROM Organism"
    row_count = db_dots.rowcount(sql_query)
    return row_count


def create_protein_file(db_config, taxonomy_id, org_version, path):
    db_dots = create_db_connection(db_config)
    query = "select nf.feature_type, nf.name, p.description, p.gene_instance_id, p.sequence from " \
            "NASequenceImp ns, NAFeatureImp nf, GeneInstance gi, Protein p where ns.taxon_id = {} " \
            "and ns.sequence_version = {} and ns.sequence_type_id = 6 and nf.na_sequence_id = ns.na_sequence_id" \
            " and nf.feature_type = 'mRNA' and gi.na_feature_id = nf.na_feature_id  and " \
            "p.gene_instance_id = gi.gene_instance_id".format(taxonomy_id, org_version)

    result = db_dots.query(query)
    fh = open(path, 'w')
    for i, value in enumerate(result):
        header_text = ">{};gi='{}'\n{}\n".format(value['name'], value['gene_instance_id'], value['sequence'])
        fh.write(header_text)


def find_organism_type(taxonomy_dct, organism, db_config):
    """
    This function finds organism type i.e. euk/gram+/gram-
    :return euk/gram+/gram-:
    """
    organism_type = 'euk'
    if 'superkingdom' in taxonomy_dct:
        if taxonomy_dct['superkingdom'] == 'Bacteria':
            organism_type = 'gram+'
            db = create_db_connection_shared_resource(db_config)
            query = "select STRAIN_TYPE from GramStrain where organism like '%{}%'".format(organism)
            result = db.query_one(query)
            if result is not None:
                strain_type = result['STRAIN_TYPE']
                if strain_type == 'Gram negative':
                    organism_type = 'gram-'
                else:
                    organism_type = "gram+"
        else:
            organism_type = 'euk'

        return organism_type
    else:
        return organism_type


class OrganismInfo:
    def __init__(self, organism, taxonomy_id, version):
        self.organism = organism
        self.taxonomy_id = taxonomy_id
        self.version = version

    @property
    def prefix(self):
        org = re.split(r'\s+', self.organism)
        if len(org) >= 2:
            species = org[0]
            genus = org[1]

            spc = list(species)
            genus = list(genus)
            taxonomy_detail = ''
            if len(org) == 4:
                taxonomy_detail = org[2] + org[3]
            elif len(org) == 3:
                taxonomy_detail = org[2]

            sp = spc[0] + spc[1] + spc[2]
            gen = genus[0] + genus[1] + "_"
            taxonomy_detail = re.sub(r'\s+', "", taxonomy_detail)
            gene_name = sp + gen + taxonomy_detail
            return gene_name

    @property
    def org_short_name(self):
        if self.prefix.endswith('_'):
            org_name = '{}v{}'.format(self.prefix, self.version)
        else:
            org_name = '{}_v{}'.format(self.prefix, self.version)
        return org_name


class NoneDict(dict):
    def __getitem__(self, key):
        return dict.get(self, key)
