--
-- core Schema
--

DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `user_ID` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contact_ID` int(11) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `tableinfo`;
CREATE TABLE `tableinfo` (
  `table_ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `table_type` varchar(50) NOT NULL,
  `primary_key_column` varchar(50) DEFAULT NULL,
  `is_versioned` tinyint(1) NOT NULL,
  `is_view` tinyint(1) NOT NULL,
  `view_on_table_ID` int(11) DEFAULT NULL,
  `superclass_table_ID` int(11) DEFAULT NULL,
  `is_updatable` tinyint(1) NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`table_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `useruploadtrack`;
CREATE TABLE `useruploadtrack` (
  `user_upload_track_ID` int(11) NOT NULL AUTO_INCREMENT,
  `user_ID` int(11) NOT NULL,
  `table_ID` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `no_of_records` int(10) NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_upload_track_ID`),
  FOREIGN KEY(`table_ID`) REFERENCES tableinfo(`table_ID`),
  FOREIGN KEY(`user_ID`) REFERENCES userinfo(`user_ID`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;



--
-- SRES Schema- Shared resources
--

DROP TABLE IF EXISTS `organism`;
CREATE TABLE IF NOT EXISTS `organism`(
    organism_ID INT(11) NOT NULL AUTO_INCREMENT,
    taxon_ID INT(11) NOT NULL,
    taxon_name VARCHAR(100) NOT NULL,
    species VARCHAR(100) NOT NULL,
    strain VARCHAR(100) NULL,
    phylum VARCHAR(100) NULL,
    family VARCHAR(100) NULL,
    genus VARCHAR(100) NULL,
    orders VARCHAR(100) NULL,
    class varchar(100) NULL,
    superkingdom VARCHAR(100) NULL,
    version FLOAT NOT NULL DEFAULT 1,
    new_version FLOAT NULL,
    comment VARCHAR(100) NULL,
    createdat TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (organism_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;


DROP TABLE IF EXISTS `geneticcode`;
CREATE TABLE `geneticcode` (
  `geneticcode_ID` int(11) NOT NULL AUTO_INCREMENT,
  `ncbi_geneticcode_ID` int(11) NOT NULL,
  `abbreviation` varchar(255) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `starts` varchar(255) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`geneticcode_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `go_term`;
CREATE TABLE `go_term` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `term_type` varchar(55) NOT NULL,
  `acc` varchar(255) NOT NULL,
  `is_obsolete` int(11) NOT NULL DEFAULT '0',
  `is_root` int(11) NOT NULL DEFAULT '0',
  `is_relation` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `acc` (`acc`),
  UNIQUE KEY `t0` (`id`),
  KEY `t1` (`name`),
  KEY `t2` (`term_type`),
  KEY `t3` (`acc`),
  KEY `t4` (`id`,`acc`),
  KEY `t5` (`id`,`name`),
  KEY `t6` (`id`,`term_type`),
  KEY `t7` (`id`,`acc`,`name`,`term_type`)
) ENGINE=MyISAM AUTO_INCREMENT=44087 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `goevidencecode`;
CREATE TABLE `goevidencecode` (
  `go_evidence_code_ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `modification_date` varchar(50) NOT NULL,
  PRIMARY KEY (`go_evidence_code_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=48939 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `log_ID` int(11) NOT NULL AUTO_INCREMENT,
  `user_ID` varchar(50) NOT NULL,
  `organism_ID` varchar(100) NOT NULL,
  `min_nasequence_id` int(11) NOT NULL,
  `max_nasequence_id` int(11) NOT NULL,
  `min_nafeature_id` int(11) NOT NULL,
  `max_nafeature_id` int(11) NOT NULL,
  `min_nalocation_id` int(11) NOT NULL,
  `max_nalocation_id` int(11) NOT NULL,
  `min_gene_id` int(11) NOT NULL,
  `max_gene_id` int(11) NOT NULL,
  `min_rna_id` int(11) NOT NULL,
  `max_rna_id` int(11) NOT NULL,
  `min_protein_id` int(11) NOT NULL,
  `max_protein_id` int(11) NOT NULL,
  `min_geneinstance_id` int(11) NOT NULL,
  `max_geneinstance_id` int(11) NOT NULL,
  `min_proteininstance_id` int(11) NOT NULL,
  `max_proteininstance_id` int(11) NOT NULL,
  `min_proteininstancefeature_id` int(11) NOT NULL,
  `max_proteininstancefeature_id` int(11) NOT NULL,
  `is_uploaded_nasequenceimp` tinyint(1) NOT NULL DEFAULT '0',
  `is_uploaded_nafeatureimp` tinyint(1) NOT NULL DEFAULT '0',
  `is_uploaded_nalocation` tinyint(1) NOT NULL DEFAULT '0',
  `is_uploaded_gene` tinyint(1) NOT NULL DEFAULT '0',
  `is_uploaded_rna` tinyint(1) NOT NULL DEFAULT '0',
  `is_uploaded_protein` tinyint(1) NOT NULL DEFAULT '0',
  `is_uploaded_geneinstance` tinyint(1) NOT NULL DEFAULT '0',
  `is_uploaded_proteininstance` tinyint(1) NOT NULL DEFAULT '0',
  `is_uploaded_proteininstancefeature` tinyint(1) NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `taxon`;
CREATE TABLE IF NOT EXISTS `taxon` (
	ncbi_taxon_ID INT(11) NOT NULL,
	parent_ID INT(11) DEFAULT NULL,
	taxon_name VARCHAR(255) NOT NULL,
	taxon_strain VARCHAR(255) NULL,
	`rank` VARCHAR(255) NOT NULL,
	genetic_code_ID INT(11) NOT NULL,
	mitochondrial_genetic_code_ID INT(11) NOT NULL,
	modification_date DATE,
	PRIMARY KEY (ncbi_taxon_ID),
    FOREIGN KEY (genetic_code_ID) REFERENCES geneticcode(geneticcode_ID),
    FOREIGN KEY (mitochondrial_genetic_code_ID) REFERENCES geneticcode(geneticcode_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `reviewstatus`;
CREATE TABLE `reviewstatus` (
  `review_status_ID` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `row_user_id` int(11) NOT NULL,
  `row_group_id` int(3) NOT NULL,
  `row_project_id` int(3) NOT NULL,
  `row_alg_invocation_id` int(11) NOT NULL,
  `email_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`review_status_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `gramstrain`;
CREATE TABLE IF NOT EXISTS `gramstrain`(
    gram_strain_ID INT(11) NOT NULL AUTO_INCREMENT,
    organism VARCHAR(255) NOT NULL,
    taxon_id INT(11) NOT NULL,
    strain_type VARCHAR(100) NOT NULL,
    membrane_type VARCHAR(100) NULL,
    modification_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (gram_strain_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;


--
-- Dots Schema - It has tables and views
--

--
-- Tables
--


DROP TABLE IF EXISTS `sequencetype`;
CREATE TABLE `sequencetype` (
  `sequence_type_ID` int(11) NOT NULL AUTO_INCREMENT,
  `sub_type` int(11) DEFAULT NULL,
  `strand` varchar(10) DEFAULT NULL,
  `hierarchy` int(5) NULL,
  `parent_sequence_type_ID` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sequence_type_ID`),
  KEY `SEQUENCETYPE_FK` (`parent_sequence_type_ID`),
  CONSTRAINT `SEQUENCETYPE_FK` FOREIGN KEY (`parent_sequence_type_ID`) REFERENCES `sequencetype` (`sequence_type_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `sequencetype` (sequence_type_ID, name, description, parent_sequence_type_ID) VALUES
(1, 'Chromosomes', 'Finished Genome', 1),
(2, 'Scaffold', 'Draft Genome', 1),
(3, 'Genomic contif','genomics contig', 1),
(4, 'EST contig', 'Est contig', 1),
(5, 'EST', 'EST', 1),
(6, 'Transcript', 'Transcript', 1),
(7, 'Protein Sequence', 'Protein Sequence', 6);


DROP TABLE IF EXISTS `nasequenceimp`;
CREATE TABLE `nasequenceimp` (
  `na_sequence_ID` int(11) NOT NULL AUTO_INCREMENT,
  `sequence_version` float NOT NULL DEFAULT '1',
  `subclass_view` varchar(50) DEFAULT NULL,
  `sequence_type_ID` int(11) DEFAULT NULL,
  `taxon_ID` int(11) DEFAULT NULL,
  `sequence` mediumtext,
  `length` int(12) DEFAULT NULL,
  `a_count` int(12) DEFAULT NULL,
  `t_count` int(12) DEFAULT NULL,
  `g_count` int(12) DEFAULT NULL,
  `c_count` int(12) DEFAULT NULL,
  `other_count` int(12) DEFAULT NULL,
  `description` varchar(2000) DEFAULT NULL,
  `external_database_ID` int(11) DEFAULT NULL,
  `source_na_sequence_ID` int(11) DEFAULT NULL,
  `sequence_piece_ID` int(111) DEFAULT NULL,
  `sequencing_center_contact_ID` int(11) DEFAULT NULL,
  `string1` varchar(255) NOT NULL,
  `string2` varchar(255) NOT NULL,
  `string3` varchar(255) NOT NULL,
  `string4` varchar(255) NOT NULL,
  `string5` varchar(255) NOT NULL,
  `tinyint1` int(5) NOT NULL,
  `nsint1` int(15) NOT NULL,
  `nsint2` int(15) NOT NULL,
  `nsint3` int(15) NOT NULL,
  `nsint4` int(15) NOT NULL,
  `int5` int(15) NOT NULL,
  `bit1` tinyint(1) NOT NULL,
  `clob1` date NOT NULL,
  `clob2` text NOT NULL,
  `clob3` text NOT NULL,
  `clob4` text NOT NULL,
  `date1` date NOT NULL,
  `date2` date NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`na_sequence_ID`),
  KEY `nasequenceimp_FK02` (`taxon_ID`),
  KEY `nasequenceimp_FK03` (`external_database_ID`),
  FOREIGN KEY (`sequence_type_ID`) REFERENCES `sequencetype`(`sequence_type_ID`),
  FOREIGN KEY (`source_na_sequence_ID`) REFERENCES `nasequenceimp`(`na_sequence_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE VIEW externalnasequence AS
SELECT
    na_sequence_ID,
    sequence_version,
    sequence_type_ID,
    taxon_ID,
    sequence,
    length,
    a_count,
    c_count,
    g_count,
    t_count,
    other_count,
    description,
    subclass_view
FROM nasequenceimp;


DROP TABLE IF EXISTS `nafeatureimp`;
CREATE TABLE IF NOT EXISTS `nafeatureimp`(
    na_feature_ID INT(11) NOT NULL AUTO_INCREMENT,
    na_sequence_ID INT(11) NOT NULL,
    subclass_view VARCHAR(50),
    feature_type VARCHAR(50) NOT NULL,
    name VARCHAR(150) NULL,
    parent_ID INT(11) NULL,
    external_database_id INT(11),
    source_id INT(11),
    prediction_algorithm_id INT(11),
    is_predicted INT(11),
    review_status_id INT(11),
    PRIMARY KEY (na_feature_ID),
    FOREIGN KEY (na_sequence_ID) REFERENCES nasequenceimp(na_sequence_ID),
    FOREIGN KEY (parent_ID) REFERENCES nafeatureimp(na_feature_ID) ON DELETE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT = 1;


DROP TABLE IF EXISTS `nalocation`;
CREATE TABLE IF NOT EXISTS `nalocation`(
    na_location_ID INT(11) NOT NULL AUTO_INCREMENT,
    na_feature_ID INT(11) NOT NULL,
    start_min INT(11),
    start_max INT(11),
    end_min INT(11),
    end_max INT(11),
    loc_order INT(3),
    is_reversed INT(3),
    is_excluded INT(3),
    literal_sequence VARCHAR(255),
    location_type VARCHAR(50),
    PRIMARY KEY(na_location_ID),
    FOREIGN KEY(na_feature_ID) REFERENCES nafeatureimp(na_feature_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;


DROP TABLE IF EXISTS `genecategory`;
CREATE TABLE `genecategory` (
  `gene_category_ID` int(11) NOT NULL,
  `term` varchar(80) NOT NULL,
  `definition` varchar(255) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`gene_category_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `gene`;
CREATE TABLE `gene` (
  `gene_ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `gene_symbol` varchar(50) DEFAULT NULL,
  `gene_category_ID` int(11) DEFAULT NULL,
  `review_status_ID` int(11) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `reviewer_summary` varchar(4000) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`gene_ID`),
  KEY `gene_FK01` (`gene_category_ID`),
  KEY `gene_FK02` (`review_status_ID`),
  CONSTRAINT `gene_FK01` FOREIGN KEY (`gene_category_ID`) REFERENCES `genecategory` (`gene_category_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=510783 DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `geneinstance`;
CREATE TABLE IF NOT EXISTS `geneinstance`(
    gene_instance_ID INT(11) NOT NULL AUTO_INCREMENT,
    na_feature_ID INT(11),
    description VARCHAR(255),
    reviewer_summary VARCHAR(255),
    is_reference INT(11),
    review_status_id INT(11),
    modification_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (gene_instance_ID),
    FOREIGN KEY(na_feature_ID) REFERENCES nafeatureimp(na_feature_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `rna`;
CREATE TABLE `rna` (
  `rna_ID` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(500) DEFAULT NULL,
  `review_status_ID` int(11) NOT NULL,
  `gene_ID` int(11) DEFAULT NULL,
  `reviewer_summary` varchar(4000) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`rna_ID`),
  KEY `RNA_FK01` (`review_status_ID`),
  KEY `RNA_FK02` (`gene_ID`),
  CONSTRAINT `RNA_FK02` FOREIGN KEY (`gene_ID`) REFERENCES `gene` (`gene_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=510783 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `blatalignment`;
CREATE TABLE `blatalignment` (
  `blat_alignment_ID` int(11) NOT NULL AUTO_INCREMENT,
  `query_na_sequence_ID` int(11) NOT NULL,
  `target_na_sequence_ID` int(11) NOT NULL,
  `query_table_ID` int(11) DEFAULT NULL,
  `query_taxon_ID` int(11) DEFAULT NULL,
  `query_external_db_ID` int(11) DEFAULT NULL,
  `target_table_ID` int(11) DEFAULT NULL,
  `target_taxon_ID` int(11) DEFAULT NULL,
  `target_external_db_ID` int(11) DEFAULT NULL,
  `is_consistent` tinyint(1) NOT NULL,
  `is_genomic_contaminant` tinyint(1) NOT NULL,
  `unaligned_3p_bases` int(11) NOT NULL,
  `unaligned_5p_bases` int(11) NOT NULL,
  `has_3p_polya` tinyint(1) NOT NULL,
  `has_5p_polya` tinyint(1) NOT NULL,
  `is_3p_complete` tinyint(1) NOT NULL,
  `is_5p_complete` tinyint(1) NOT NULL,
  `percent_IDentity` int(10) NOT NULL,
  `max_query_gap` int(10) NOT NULL,
  `max_target_gap` int(10) NOT NULL,
  `number_of_spans` int(10) NOT NULL,
  `query_start` int(10) NOT NULL,
  `query_end` int(10) NOT NULL,
  `target_start` int(10) NOT NULL,
  `target_end` int(10) NOT NULL,
  `is_reversed` tinyint(1) NOT NULL,
  `query_bases_aligned` int(10) NOT NULL,
  `repeat_bases_aligned` int(10) NOT NULL,
  `num_ns` int(10) NOT NULL,
  `score` float NOT NULL,
  `is_best_alignment` tinyint(1) NOT NULL DEFAULT '0',
  `blat_alignment_quality_ID` int(10) NOT NULL,
  `blocksizes` varchar(4000) NOT NULL,
  `qstarts` varchar(4000) NOT NULL,
  `tstarts` varchar(4000) NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`blat_alignment_ID`),
  KEY `blatalignment_FK01` (`query_na_sequence_ID`),
  KEY `blatalignment_FK02` (`target_na_sequence_ID`),
  KEY `blatalignment_FK07` (`target_taxon_ID`),
  KEY `blatalignment_FK08` (`target_external_db_ID`),
  KEY `blatalignment_FK09` (`blat_alignment_quality_ID`),
  KEY `blatalignment_FK04` (`query_taxon_ID`),
  KEY `blatalignment_FK05` (`query_external_db_ID`),
  KEY `blatalignment_FK03` (`query_table_ID`),
  KEY `blatalignment_FK06` (`target_table_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `pathway`;
CREATE TABLE `pathway` (
  `pathway_ID` int(11) NOT NULL AUTO_INCREMENT,
  `taxon_ID` int(11) NOT NULL,
  `version` float NOT NULL,
  `url` text NOT NULL,
  PRIMARY KEY (`pathway_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `pathway_data`;
CREATE TABLE `pathway_data` (
  `pathway_ID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `na_sequence_ID` int(11) NOT NULL,
  `ko_id` varchar(50) NOT NULL,
  `url` varchar(500) NOT NULL,
  `taxon_ID` int(11) DEFAULT NULL,
  `version` float NOT NULL DEFAULT '1',
  PRIMARY KEY (`pathway_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `pdomain_join`;
CREATE TABLE `pdomain_join` (
  `na_sequence_ID` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `domain_name` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `taxon_ID` int(11) DEFAULT NULL,
  `sequence_version` float NOT NULL DEFAULT '0',
  `product` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `species` varchar(100) NOT NULL,
  `strain` varchar(100) DEFAULT NULL,
  `new_version` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `protein`;
CREATE TABLE IF NOT EXISTS `protein`(
    protein_ID INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(255),
    review_status_ID INT(11),
    reviewer_summary VARCHAR(255),
    gene_instance_ID INT(11),
    sequence TEXT NOT NULL,
    PRIMARY KEY (protein_ID),
    FOREIGN KEY(gene_instance_ID) REFERENCES geneinstance(gene_instance_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;



DROP TABLE IF EXISTS `protein_cluster`;
CREATE TABLE `protein_cluster` (
  `protein_cluster_ID` int(11) NOT NULL AUTO_INCREMENT,
  `cluster_ID` int(11) NOT NULL,
  `gene_ID` int(11) NOT NULL,
  `taxon_ID` int(11) NOT NULL,
  `desc` varchar(100) NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`protein_cluster_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=45475 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `proteininstancefeature`;
CREATE TABLE `proteininstancefeature` (
  `protein_instance_feature_ID` int(11) NOT NULL AUTO_INCREMENT,
  `protein_instance_ID` int(11) NOT NULL,
  `feature_name` varchar(255) NOT NULL,
  `subclass_view` varchar(255) DEFAULT NULL,
  `location_start` int(10) DEFAULT NULL,
  `location_stop` int(10) DEFAULT NULL,
  `length` int(10) DEFAULT NULL,
  `prediction_algorithm_id` int(11) DEFAULT NULL,
  `pval_mant` float DEFAULT NULL,
  `pval_exp` int(10) DEFAULT NULL,
  `bit_score` float DEFAULT NULL,
  `domain_name` varchar(1000) DEFAULT NULL,
  `prediction_id` varchar(100) DEFAULT NULL,
  `go_id` varchar(100) DEFAULT NULL,
  `is_reviewed` tinyint(1) DEFAULT NULL,
  `algorithm_id` int(11) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`protein_instance_feature_ID`),
  KEY `proteininstancefeature_FK01` (`protein_instance_ID`),
  KEY `proteininstancefeature_FK02` (`prediction_algorithm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1942002 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `signalp`;
CREATE TABLE IF NOT EXISTS `signalp`(
signalp_ID INT(11) NOT NULL AUTO_INCREMENT,
gene_instance_ID INT(11) NOT NULL,
`y-score` FLOAT NULL,
`y-pos` INT(11) NULL,
`d-score` FLOAT NULL,
status varchar(20) NULL,
PRIMARY KEY(signalp_ID),
FOREIGN KEY(gene_instance_id) REFERENCES geneinstance(gene_instance_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `tmhmm`;
CREATE TABLE IF NOT EXISTS `tmhmm`(
tmhmm_ID INT(11) NOT NULL AUTO_INCREMENT,
gene_instance_ID INT(11) NOT NULL,
inside VARCHAR(60),
outside VARCHAR(60),
tmhelix VARCHAR(60),
modification_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(tmhmm_ID),
FOREIGN KEY(gene_instance_ID) REFERENCES geneinstance(gene_instance_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `hmmpfam`;
CREATE TABLE IF NOT EXISTS `hmmpfam`(
    pfam_ID INT(11) NOT NULL AUTO_INCREMENT,
    gene_instance_ID INT(11) NOT NULL,
    e_value FLOAT,
    score FLOAT,
    bias FLOAT,
    accession_id VARCHAR(100),
    domain_name VARCHAR(1000),
    domain_description VARCHAR(1000),
    modification_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(pfam_ID),
    FOREIGN KEY(gene_instance_ID) REFERENCES geneinstance(gene_instance_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `interproscan`;
CREATE TABLE IF NOT EXISTS `interproscan`(
interpro_scan_ID INT(11) NOT NULL AUTO_INCREMENT,
gene_instance_ID INT(11) NOT NULL,
feature_name VARCHAR(255) NOT NULL,
subclass_view VARCHAR(255) NULL,
location_start INT(10) NULL,
location_stop INT(10) NULL,
length INT(10) NULL,
prediction_algorithm_id INT(11) NULL,
pval_mant FLOAT NULL,
pval_exp INT(10) NULL,
bit_score FLOAT(20) NULL,
domain_name varchar(1000) NULL,
prediction_id varchar(100) NULL,
go_id varchar(100) NULL,
is_reviewed INT(1) NULL,
algorithm_id INT(11) NULL,
modification_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(interpro_scan_ID),
FOREIGN KEY(gene_instance_ID) REFERENCES geneinstance(gene_instance_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

