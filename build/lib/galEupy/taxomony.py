import re
import logging
_logger = logging.getLogger("galEupy.taxonomy")


class OrganismName:
    def __init__(self, org_name, org_version=1):
        """
        class constructor for the Organism name
        parameters
        -------------
        org_name: str
            Full name of the organism
        org_version: str
            Version string
        """
        # _logger.info(f"Organism: {org_name}, Version: {org_version}")
        self.org_name = org_name
        self.org_version = org_version
        self.org_arr = re.split(r'\s', org_name)
        self.species = "{} {}".format(self.org_arr[0], self.org_arr[1])
        self.strain = ''
        if len(self.org_arr) > 2:
            self.strain = " ".join(self.org_arr[2:])

    @property
    def prefix(self):
        """
        Returns the organism prefix
        Returns
        --------
        gene_name: str
            Organism name prefix
        """
        org = re.split(r'\s+', self.org_name)
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
        """
        Return short organism name with version number
        Returns
        ----------
        org_name: str
            short organism name with organism version
        """
        if self.prefix.endswith('_'):
            org_name = f'{self.prefix}v{self.org_version}'
        else:
            org_name = f'{self.prefix}_v{self.org_version}' '{}_v{}'
        return org_name


class CommonOrganismInfo(OrganismName):
    def __init__(self, db_sres, org_name, org_version=1):
        OrganismName.__init__(self, org_name, org_version)
        self.db_sres = db_sres

    @property
    def taxonomy_id_sres(self):
        sql_query = f"SELECT NCBI_TAXON_ID FROM Taxon where TAXON_NAME = '{self.org_name}'"
        data = self.db_sres.query_one(sql_query)
        if data is not None:
            taxonomy_id = data['NCBI_TAXON_ID']
            if taxonomy_id is None:
                _logger.error("Error :Organism Name has issue:")
            return taxonomy_id

    def taxon_entries(self):
        _logger.info(f'Checking similar organism entries with {self.species}')
        sql_query = f"SELECT NCBI_TAXON_ID, TAXON_NAME FROM Taxon where TAXON_NAME like '{self.species}%'"
        result = self.db_sres.query(sql_query)
        if len(result) > 0:
            result_str = "\n".join(f"{d['NCBI_TAXON_ID']}\t{d['TAXON_NAME']}" for d in result)
            _logger.info(f'Entries available:\nNCBI_TAXON_ID\tTAXON_NAME\n{result_str}')
        else:
            if len(self.org_arr) > 1 and len(self.org_arr[1]) >= 2:
                short_org_name = f'{self.org_arr[0]} {self.org_arr[1][0:2]}'
                _logger.info(f'There is no entry with species name. Listing organisms with {short_org_name}')

                sql_query = f"SELECT NCBI_TAXON_ID, TAXON_NAME FROM Taxon where TAXON_NAME like '{short_org_name}%'"
                result = self.db_sres.query(sql_query)
                if len(result) > 0:
                    result_str = "\n".join(f"{d['NCBI_TAXON_ID']}\t{d['TAXON_NAME']}" for d in result)
                    _logger.info(f'Entries available: \nNCBI_TAXON_ID\tTAXON_NAME\n{result_str}')

                else:
                    _logger.info(f'No record found with: {short_org_name}%')
        return False

    def taxonomy_hierarchy(self):
        query = f"""SELECT NCBI_TAXON_ID, PARENT_ID, TAXON_NAME, TAXON_STRAIN, `RANK`  FROM Taxon 
        where TAXON_NAME = '{self.org_name}'"""

        taxonomy_dct = {}
        result = self.db_sres.query(query)
        for i, value in enumerate(result):
            if value['RANK'] in ["species", "subspecies", "strain"]:
                taxonomy_dct['TAXON_ID'] = value['NCBI_TAXON_ID']
                taxonomy_id, parent_id, name, rank = self.fetch_taxonomy_info_by_id(value['PARENT_ID'])
                taxonomy_dct[rank] = name
                while taxonomy_id != parent_id:
                    taxonomy_id, parent_id, name, rank = self.fetch_taxonomy_info_by_id(parent_id)
                    taxonomy_dct[rank] = name
            elif value['RANK'] == 'no rank':
                taxonomy_id, parent_id, name, rank = self.fetch_taxonomy_info_by_id(value['PARENT_ID'])
                if rank == 'species':
                    taxonomy_dct['TAXON_ID'] = value['NCBI_TAXON_ID']
                    taxonomy_dct[rank] = name
                    while taxonomy_id != parent_id:
                        taxonomy_id, parent_id, name, rank = self.fetch_taxonomy_info_by_id(parent_id)
                        taxonomy_dct[rank] = name
                else:
                    _logger.error("Please check the organism name")
            elif value['RANK'] != '':
                _logger.error("Please check the organism name")
        return taxonomy_dct

    def fetch_taxonomy_info_by_id(self, taxonomy_id):
        child_query = f"""SELECT NCBI_TAXON_ID, PARENT_ID, TAXON_NAME, TAXON_STRAIN, `RANK`  FROM Taxon WHERE 
        NCBI_TAXON_ID = {taxonomy_id}"""
        result = self.db_sres.query(child_query)
        for i, value in enumerate(result):
            return value['NCBI_TAXON_ID'], value['PARENT_ID'], value['TAXON_NAME'], value['RANK']

    def find_organism_type(self, taxonomy_dct):
        """
        This function finds organism type i.e. euk/gram+/gram-
        :return euk/gram+/gram-:
        """
        organism_type = 'euk'
        if 'superkingdom' in taxonomy_dct:
            if taxonomy_dct['superkingdom'] == 'Bacteria':
                organism_type = 'gram+'
                query = f"select STRAIN_TYPE from GramStrain where organism like '%{self.org_name}%'"
                result = self.db_sres.query_one(query)
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


class DotsOrganism(OrganismName):
    def __init__(self, db_dots, org_name, org_version=1):
        OrganismName.__init__(self, org_name, org_version)
        self.db_dots = db_dots

    @property
    def taxonomy_hierarchy_dots(self):
        sql_query = f"select * from Organism where TAXON_NAME = '{self.org_name}' and VERSION = {self.org_version}"
        taxonomy_dct = {}

        result = self.db_dots.query_one(sql_query)
        if result is not None:
            taxonomy_dct = result
        taxonomy_dct = NoneDict(taxonomy_dct)
        return taxonomy_dct

    def taxonomy_id_dots(self):
        taxonomy_dct = self.taxonomy_hierarchy_dots
        if 'TAXON_ID' in taxonomy_dct:
            return taxonomy_dct['TAXON_ID']

    def remove_organism_record(self):
        taxonomy_id = self.taxonomy_id_dots()

        if taxonomy_id is None:
            _logger.info(f"Organism details doesn't exist. \nOrganism name; {self.org_name}, version: {self.org_version}")
        else:
            sql_query_1 = F"""DELETE ips FROM InterProScan as ips
        INNER JOIN GeneInstance AS gi
        ON ips.gene_instance_id = gi.gene_instance_id
        INNER JOIN NAFeatureImp as nf
        ON gi.na_feature_id = nf.na_feature_id
        INNER JOIN NASequenceImp as ns 
        ON nf.na_sequence_id = ns.na_sequence_id 
        WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id = 6"""
            self.db_dots.insert(sql_query_1)

            sql_query_2 = F"""DELETE sp FROM SignalP as sp
        INNER JOIN GeneInstance AS gi
        ON sp.gene_instance_id = gi.gene_instance_id
        INNER JOIN NAFeatureImp as nf
        ON gi.na_feature_id = nf.na_feature_id
        INNER JOIN NASequenceImp as ns 
        ON nf.na_sequence_id = ns.na_sequence_id 
        WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id = 6"""
            self.db_dots.insert(sql_query_2)

            sql_query_3 = F"""DELETE tm FROM Tmhmm as tm
        INNER JOIN GeneInstance AS gi
        ON tm.gene_instance_id = gi.gene_instance_id
        INNER JOIN NAFeatureImp as nf
        ON gi.na_feature_id = nf.na_feature_id
        INNER JOIN NASequenceImp as ns 
        ON nf.na_sequence_id = ns.na_sequence_id 
        WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id = 6"""
            self.db_dots.insert(sql_query_3)

            sql_query_4 = F"""DELETE p,gi FROM Protein as p
        INNER JOIN GeneInstance AS gi
        ON p.gene_instance_id = gi.gene_instance_id
        INNER JOIN NAFeatureImp as nf
        ON gi.na_feature_id = nf.na_feature_id
        INNER JOIN NASequenceImp as ns 
        ON nf.na_sequence_id = ns.na_sequence_id 
        WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id = 6"""
            self.db_dots.insert(sql_query_4)

            # NaLocation
            sql_query_5 = F"""DELETE nl,nf FROM NALocation as nl
            INNER JOIN NAFeatureImp as nf
            ON nl.na_feature_id = nf.na_feature_id
            INNER JOIN NASequenceImp as ns 
            ON nf.na_sequence_id = ns.na_sequence_id 
            WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and sequence_type_id != 1"""
            self.db_dots.insert(sql_query_5)

            # Na feature
            sql_query_6 = F"""DELETE nf FROM  NAFeatureImp as nf
            INNER JOIN NASequenceImp as ns 
            ON nf.na_sequence_id = ns.na_sequence_id 
            WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version}"""
            self.db_dots.insert(sql_query_6)

            # delete NasequenceImp
            sql_query_7 = F"""DELETE ns from NASequenceImp as ns 
              WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id != 1"""
            self.db_dots.insert(sql_query_7)

            # delete NasequenceImp
            sql_query_7 = F"""DELETE ns from NASequenceImp as ns 
                      WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version}"""
            self.db_dots.insert(sql_query_7)

            # Delete Organism table
            sql_query_9 = F"""DELETE org from Organism as org 
            WHERE org.taxon_id = {taxonomy_id} and org.version = {self.org_version}"""
            self.db_dots.insert(sql_query_9)

    def get_organism_record(self):

        count_dct = {}
        taxonomy_id = self.taxonomy_id_dots()
        if taxonomy_id is None:
            _logger.info(f"Organism details doesn't exist. \nOrganism name; {self.org_name}, version: {self.org_version}")
        else:
            sql_query_1 = F"""select count(*) as count FROM InterProScan as ips
        INNER JOIN GeneInstance AS gi
        ON ips.gene_instance_id = gi.gene_instance_id
        INNER JOIN NAFeatureImp as nf
        ON gi.na_feature_id = nf.na_feature_id
        INNER JOIN NASequenceImp as ns 
        ON nf.na_sequence_id = ns.na_sequence_id 
        WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id = 6"""
            data1 = self.db_dots.query_one(sql_query_1)
            count_dct['InterProScan'] = data1['count']

            sql_query_2 = F"""SELECT COUNT(*) AS count FROM SignalP as sp
        INNER JOIN GeneInstance AS gi
        ON sp.gene_instance_id = gi.gene_instance_id
        INNER JOIN NAFeatureImp as nf
        ON gi.na_feature_id = nf.na_feature_id
        INNER JOIN NASequenceImp as ns 
        ON nf.na_sequence_id = ns.na_sequence_id 
        WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id = 6"""
            data1 = self.db_dots.query_one(sql_query_2)
            count_dct['SignalP'] = data1['count']

            sql_query_3 = F"""SELECT COUNT(*) AS count FROM Tmhmm as tm
        INNER JOIN GeneInstance AS gi
        ON tm.gene_instance_id = gi.gene_instance_id
        INNER JOIN NAFeatureImp as nf
        ON gi.na_feature_id = nf.na_feature_id
        INNER JOIN NASequenceImp as ns 
        ON nf.na_sequence_id = ns.na_sequence_id 
        WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id = 6"""
            data1 = self.db_dots.query_one(sql_query_3)
            count_dct['Tmhmm'] = data1['count']

            sql_query_4 = F"""SELECT COUNT(*) AS count FROM HmmPfam as hfam
        INNER JOIN GeneInstance AS gi
        ON hfam.gene_instance_id = gi.gene_instance_id
        INNER JOIN NAFeatureImp as nf
        ON gi.na_feature_id = nf.na_feature_id
        INNER JOIN NASequenceImp as ns 
        ON nf.na_sequence_id = ns.na_sequence_id 
        WHERE ns.taxon_id = {taxonomy_id} and ns.sequence_version = {self.org_version} and ns.sequence_type_id = 6"""
            data1 = self.db_dots.query_one(sql_query_4)
            count_dct['HmmPfam'] = data1['count']

            _logger.info(f"""Count of rows for Organism Name: {self.org_name}, Organism Version: {self.org_version}
                        HmmPfam: {count_dct['HmmPfam']}
                        SignalP: {count_dct['SignalP']}
                        Tmhmm: {count_dct['Tmhmm']}
                        InterProScan: {count_dct['InterProScan']}
            """)


class Taxonomy(CommonOrganismInfo, DotsOrganism):
    def __init__(self, db_sres, db_dots, org_name, org_version=1):
        CommonOrganismInfo.__init__(self, db_sres, org_name, org_version)
        DotsOrganism.__init__(self, db_dots, org_name, org_version)

    def update_organism_table(self):
        _logger.info(f"Updating the organism table. \nOrganism name: {self.org_name}\nversion: {self.org_version}")

        taxonomy_dct = self.taxonomy_hierarchy()
        taxonomy_dct = NoneDict(taxonomy_dct)
        taxonomy_id = taxonomy_dct['TAXON_ID']
        genus = taxonomy_dct['genus']
        order = taxonomy_dct['order']
        phylum = taxonomy_dct['phylum']
        class_name = taxonomy_dct['class']
        # subclass = taxonomy_dct['subclass']
        family = taxonomy_dct['family']
        super_kingdom = taxonomy_dct['superkingdom']

        query = f'''INSERT INTO Organism(TAXON_ID, TAXON_NAME, SPECIES, STRAIN, PHYLUM, FAMILY, GENUS, ORDERS, CLASS, 
        SUPERKINGDOM, VERSION) VALUES ({taxonomy_id}, '{self.org_name}', '{self.species}', '{self.strain}', '{phylum}',
        '{family}', '{genus}', '{order}', '{class_name}', '{super_kingdom}', '{self.org_version}')'''
        self.db_dots.insert(query)
        _logger.info(" Organism Table update complete")
        return taxonomy_dct

    @property
    def organism_existence(self):
        _logger.debug("checking the organism existence in organism table")
        if not self.org_name:
            _logger.info("Error: Organism Name does not exist")
            return True
        else:
            _logger.info(f'Organism: {self.org_name} version: {self.org_version}')
            taxonomy_id = self.taxonomy_id_sres
            if taxonomy_id:
                sql_query = f"select * from Organism where TAXON_ID = {taxonomy_id} and VERSION = {self.org_version}"
                row_count = self.db_dots.rowcount(sql_query)
                if row_count == 1:
                    _logger.info("Error: Organism Name and same version already exists")
                    return True
                else:
                    _logger.info("New Organism")
                    return False
            else:
                _logger.info("Error: Please check the organism name")
                return True


    def organism_name_check(self):
        sql_query = f"select * from Organism where TAXON_ID = {taxonomy_id} and VERSION = {self.org_version}"

    @property
    def organism_type(self):
        organism_type = self.find_organism_type(self.taxonomy_hierarchy_dots)
        return organism_type


class NoneDict(dict):
    def __getitem__(self, key):
        return dict.get(self, key)
