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
    assembly_accession VARCHAR(50) NULL,
    assembly_name VARCHAR(50) NULL,
    assembly_level VARCHAR(50) NULL,
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


DROP TABLE IF EXISTS `aafeatureimp`;
CREATE TABLE IF NOT EXISTS `aafeatureimp` (
  `aa_feature_ID` int(11) NOT NULL AUTO_INCREMENT,
  `aa_sequence_ID` int(11) NOT NULL,
  `parent_ID` int(11) DEFAULT NULL,
  `na_feature_ID` int(11) DEFAULT NULL,
  `subclass_view` varchar(50) DEFAULT NULL,
  `description` varchar(4000) DEFAULT NULL,
  `motif_aa_sequence_ID` int(11) DEFAULT NULL,
  `external_database_ID` int(11) DEFAULT NULL,
  `source_ID` int(11) DEFAULT NULL,
  `prediction_algorithm_ID` int(11) DEFAULT NULL,
  `is_predicted` tinyint(1) NOT NULL,
  `int1` int(11) DEFAULT NULL,
  `int2` int(11) DEFAULT NULL,
  `int3` int(11) DEFAULT NULL,
  `int4` int(11) DEFAULT NULL,
  `int5` int(11) DEFAULT NULL,
  `int6` int(11) DEFAULT NULL,
  `int7` int(11) DEFAULT NULL,
  `int8` int(11) DEFAULT NULL,
  `int9` int(11) DEFAULT NULL,
  `int10` int(11) DEFAULT NULL,
  `tinyint1` int(5) DEFAULT NULL,
  `tinyint2` int(5) DEFAULT NULL,
  `tinyint3` int(5) DEFAULT NULL,
  `tinyint4` int(5) DEFAULT NULL,
  `tinyint5` int(5) DEFAULT NULL,
  `tinyint6` int(5) DEFAULT NULL,
  `float1` double DEFAULT NULL,
  `float2` double DEFAULT NULL,
  `float3` double DEFAULT NULL,
  `float4` double DEFAULT NULL,
  `float5` double DEFAULT NULL,
  `float6` double DEFAULT NULL,
  `string1` varchar(255) DEFAULT NULL,
  `string2` varchar(255) DEFAULT NULL,
  `string3` varchar(255) DEFAULT NULL,
  `string4` varchar(255) DEFAULT NULL,
  `string5` varchar(255) DEFAULT NULL,
  `string6` varchar(255) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`aa_feature_ID`),
  KEY `aafeatureimp_FK01` (`aa_sequence_ID`),
  KEY `aafeatureimp_FK02` (`parent_ID`),
  KEY `aafeatureimp_FK03` (`na_feature_ID`),
  KEY `aafeatureimp_FK04` (`motif_aa_sequence_ID`),
  KEY `aafeatureimp_FK05` (`external_database_ID`),
  KEY `aafeatureimp_FK06` (`prediction_algorithm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `aasequenceimp`
--

DROP TABLE IF EXISTS `aasequenceimp`;
CREATE TABLE IF NOT EXISTS `aasequenceimp` (
  `aa_sequence_id` int(11) NOT NULL AUTO_INCREMENT,
  `sequence_version` int(10) DEFAULT '1',
  `subclass_view` varchar(50) NOT NULL,
  `molecular_weight` int(20) DEFAULT NULL,
  `sequence` longtext,
  `length` int(15) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `external_database_id` int(11) DEFAULT NULL,
  `source_id` int(11) DEFAULT NULL,
  `source_aa_sequence_id` int(11) DEFAULT NULL,
  `tinyint1` int(5) DEFAULT NULL,
  `string1` varchar(255) DEFAULT NULL,
  `string2` varchar(255) DEFAULT NULL,
  `string3` varchar(255) DEFAULT NULL,
  `string4` varchar(255) DEFAULT NULL,
  `int1` int(11) DEFAULT NULL,
  `int2` int(11) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`aa_sequence_id`),
  KEY `aasequenceimp_FK01` (`external_database_id`),
  KEY `aasequenceimp_FK02` (`source_aa_sequence_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;



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


DROP TABLE IF EXISTS `nafeatureimp`;
CREATE TABLE IF NOT EXISTS `nafeatureimp`(
    na_feature_ID INT(11) NOT NULL AUTO_INCREMENT,
    na_sequence_ID INT(11) NOT NULL,
    subclass_view VARCHAR(50),
    feature_type VARCHAR(50) NOT NULL,
    name VARCHAR(150) NULL,
    sequence_ontology_ID int(11) DEFAULT NULL,
    parent_ID INT(11) NULL,
    external_database_id INT(11),
    source_id INT(11),
    prediction_algorithm_id INT(11),
    is_predicted INT(11),
    review_status_id INT(11),
    `nfint1` int(11) DEFAULT NULL,
  `nfint2` int(11) DEFAULT NULL,
  `nfint3` int(11) DEFAULT NULL,
  `nfint4` int(11) DEFAULT NULL,
  `int5` int(11) DEFAULT NULL,
  `int6` int(11) DEFAULT NULL,
  `tinyint1` int(5) DEFAULT NULL,
  `tinyint2` int(5) DEFAULT NULL,
  `tinyint3` int(5) DEFAULT NULL,
  `tinyint4` int(5) DEFAULT NULL,
  `tinyint5` int(5) DEFAULT NULL,
  `tinyint6` int(5) DEFAULT NULL,
  `float1` double DEFAULT NULL,
  `float2` double DEFAULT NULL,
  `float3` double DEFAULT NULL,
  `nffloat4` double DEFAULT NULL,
  `float5` double DEFAULT NULL,
  `float6` double DEFAULT NULL,
  `text1` varchar(1000) DEFAULT NULL,
  `string1` varchar(1000) DEFAULT NULL,
  `string2` varchar(255) DEFAULT NULL,
  `string3` varchar(255) DEFAULT NULL,
  `string4` varchar(255) DEFAULT NULL,
  `string5` varchar(1000) DEFAULT NULL,
  `string6` varchar(255) DEFAULT NULL,
  `string7` varchar(255) DEFAULT NULL,
  `string8` varchar(255) DEFAULT NULL,
  `string9` varchar(1000) DEFAULT NULL,
  `string10` varchar(255) DEFAULT NULL,
  `string11` varchar(255) DEFAULT NULL,
  `string12` varchar(255) DEFAULT NULL,
  `string13` varchar(255) DEFAULT NULL,
  `string14` varchar(500) DEFAULT NULL,
  `string15` varchar(255) DEFAULT NULL,
  `string16` varchar(255) DEFAULT NULL,
  `string17` varchar(255) DEFAULT NULL,
  `string18` varchar(255) DEFAULT NULL,
  `string19` varchar(255) DEFAULT NULL,
  `string20` varchar(1000) DEFAULT NULL,
  `string21` varchar(255) DEFAULT NULL,
  `string22` varchar(255) DEFAULT NULL,
  `string23` varchar(255) DEFAULT NULL,
  `string24` varchar(255) DEFAULT NULL,
  `string25` varchar(255) DEFAULT NULL,
  `string26` varchar(255) DEFAULT NULL,
  `string27` varchar(255) DEFAULT NULL,
  `string28` varchar(255) DEFAULT NULL,
  `string29` varchar(255) DEFAULT NULL,
  `string30` varchar(64) DEFAULT NULL,
  `string31` varchar(64) DEFAULT NULL,
  `string32` varchar(64) DEFAULT NULL,
  `string33` varchar(64) DEFAULT NULL,
  `string34` varchar(64) DEFAULT NULL,
  `string35` varchar(64) DEFAULT NULL,
  `string36` varchar(64) DEFAULT NULL,
  `string37` varchar(64) DEFAULT NULL,
  `string38` varchar(64) DEFAULT NULL,
  `string39` varchar(64) DEFAULT NULL,
  `string40` varchar(64) DEFAULT NULL,
  `string41` varchar(64) DEFAULT NULL,
  `string42` varchar(64) DEFAULT NULL,
  `string43` varchar(64) DEFAULT NULL,
  `string44` varchar(64) DEFAULT NULL,
  `string45` varchar(64) DEFAULT NULL,
  `string46` varchar(64) DEFAULT NULL,
  `string47` varchar(64) DEFAULT NULL,
  `string48` varchar(64) DEFAULT NULL,
  `string49` varchar(64) DEFAULT NULL,
  `string50` varchar(64) DEFAULT NULL,
   `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (na_feature_ID),
    FOREIGN KEY (na_sequence_ID) REFERENCES nasequenceimp(na_sequence_ID),
    FOREIGN KEY (parent_ID) REFERENCES nafeatureimp(na_feature_ID) ON DELETE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT = 1 ROW_FORMAT=DYNAMIC;


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
    `text1` varchar(500) DEFAULT NULL,
    `text2` varchar(500) DEFAULT NULL,
    `text3` varchar(500) DEFAULT NULL,
    `text4` varchar(500) DEFAULT NULL,
    `text5` varchar(500) DEFAULT NULL,
    `text6` varchar(500) DEFAULT NULL,
    `text7` varchar(500) DEFAULT NULL,
    `text8` varchar(500) DEFAULT NULL,
    `text9` varchar(500) DEFAULT NULL,
    `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`protein_instance_feature_ID`),
  KEY `proteininstancefeature_FK01` (`protein_instance_ID`),
  KEY `proteininstancefeature_FK02` (`prediction_algorithm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1942002 DEFAULT CHARSET=utf8;

CREATE TABLE COG_CATEGORIES (
    cog_id VARCHAR(10) PRIMARY KEY,
    description VARCHAR(255) NOT NULL
);

INSERT INTO COG_CATEGORIES (cog_id, description) VALUES
('A', 'RNA processing and modification'),
('B', 'Chromatin Structure and dynamics'),
('C', 'Energy production and conversion'),
('D', 'Cell cycle control and mitosis'),
('E', 'Amino Acid metabolism and transport'),
('F', 'Nucleotide metabolism and transport'),
('G', 'Carbohydrate metabolism and transport'),
('H', 'Coenzyme metabolism'),
('I', 'Lipid metabolism'),
('J', 'Translation'),
('K', 'Transcription'),
('L', 'Replication and repair'),
('M', 'Cell wall/membrane/envelope biogenesis'),
('N', 'Cell motility'),
('O', 'Post-translational modification, protein turnover, chaperone functions'),
('P', 'Inorganic ion transport and metabolism'),
('Q', 'Secondary Structure'),
('T', 'Signal Transduction'),
('U', 'Intracellular trafficking and secretion'),
('Y', 'Nuclear structure'),
('Z', 'Cytoskeleton'),
('R', 'General Functional Prediction only'),
('S', 'Function Unknown');


DROP TABLE IF EXISTS `KEGG`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `KEGG` AS
select
    `proteininstancefeature`.`protein_instance_feature_ID` AS `protein_instance_feature_id`,
    `proteininstancefeature`.`protein_instance_id` AS `protein_instance_id`,
    `proteininstancefeature`.`feature_name` AS `feature_name`,
    `proteininstancefeature`.`subclass_view` AS `subclass_view`,
    `proteininstancefeature`.`domain_name` AS `domain_name`,
    `proteininstancefeature`.`text1` AS `EC`,
    `proteininstancefeature`.`text2` AS `KEGG_ko`,
    `proteininstancefeature`.`text3` AS `KEGG_Pathway`,
    `proteininstancefeature`.`text4` AS `KEGG_Module`,
    `proteininstancefeature`.`text5` AS `KEGG_Reaction`,
    `proteininstancefeature`.`text6` AS `KEGG_rclass`,
    `proteininstancefeature`.`text7` AS `BRITE`,
    `proteininstancefeature`.`text8` AS `KEGG_TC`,
    `proteininstancefeature`.`prediction_id` AS `prediction_id`,
    `proteininstancefeature`.`modification_date` AS `modification_date`
from `proteininstancefeature`
where (`proteininstancefeature`.`subclass_view` = 'KEGG');




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

--
-- Structure for view `BlastProDom`
--
DROP TABLE IF EXISTS `BlastProDom`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `BlastProDom` AS
select
    `proteininstancefeature`.`protein_instance_feature_ID` AS `protein_instance_feature_id`,
    `proteininstancefeature`.`protein_instance_id` AS `protein_instance_id`,
    `proteininstancefeature`.`feature_name` AS `feature_name`,
    `proteininstancefeature`.`subclass_view` AS `subclass_view`,
    `proteininstancefeature`.`location_start` AS `location_start`,
    `proteininstancefeature`.`location_stop` AS `location_stop`,
    `proteininstancefeature`.`length` AS `length`,
    `proteininstancefeature`.`pval_mant` AS `pval_mant`,
    `proteininstancefeature`.`pval_exp` AS `pval_exp`,
    `proteininstancefeature`.`bit_score` AS `bit_score`,
    `proteininstancefeature`.`domain_name` AS `domain_name`,
    `proteininstancefeature`.`prediction_id` AS `prediction_id`,
    `proteininstancefeature`.`modification_date` AS `modification_date`
from `proteininstancefeature`
where (`proteininstancefeature`.`subclass_view` = 'BlastProDom');


--
-- Structure for view `cds`
--
DROP TABLE IF EXISTS `cds`;


CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `cds` AS
select
`nafeatureimp`.`na_feature_ID` AS `na_feature_id`,
`nafeatureimp`.`na_sequence_ID` AS `na_sequence_id`,
`nafeatureimp`.`subclass_view` AS `subclass_view`,
`nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_id`,
`nafeatureimp`.`name` AS `name`,
`nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'CDS');

-- --------------------------------------------------------


--
-- Structure for view `externalaasequence`
--
DROP TABLE IF EXISTS `externalaasequence`;


CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `externalaasequence` AS
select
    `aasequenceimp`.`aa_sequence_id` AS `aa_sequence_ID`,
    `aasequenceimp`.`subclass_view` AS `subclass_view`,
    `aasequenceimp`.`molecular_weight` AS `molecular_weight`,
    `aasequenceimp`.`sequence` AS `sequence`,
    `aasequenceimp`.`length` AS `length`,
    `aasequenceimp`.`description` AS `description`,
    `aasequenceimp`.`external_database_id` AS `external_database_ID`,
    `aasequenceimp`.`source_id` AS `source_ID`,
    `aasequenceimp`.`string1` AS `SECONDARY_IDENTIFIER`,
    `aasequenceimp`.`string2` AS `NAME`,
    `aasequenceimp`.`string3` AS `MOLECULE_TYPE`,
    `aasequenceimp`.`string4` AS `CRC32_VALUE`,
    `aasequenceimp`.`modification_date` AS `modification_date`
from `aasequenceimp`
where (`aasequenceimp`.`subclass_view` = 'externalaasequence');


-- --------------------------------------------------------

--
-- Structure for view `externalnasequence`
--
DROP TABLE IF EXISTS `externalnasequence`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `externalnasequence` AS
select
    `nasequenceimp`.`na_sequence_ID` AS `na_sequence_ID`,
    `nasequenceimp`.`sequence_version` AS `sequence_version`,
    `nasequenceimp`.`sequence_type_ID` AS `sequence_type_ID`,
    `nasequenceimp`.`external_database_ID` AS `external_database_ID`,
    `nasequenceimp`.`string1` AS `source_ID`,
    `nasequenceimp`.`string2` AS `secondary_identifier`,
    `nasequenceimp`.`string3` AS `name`,
    `nasequenceimp`.`taxon_ID` AS `taxon_ID`,
    `nasequenceimp`.`sequence` AS `sequence`,
    `nasequenceimp`.`length` AS `length`,
    `nasequenceimp`.`a_count` AS `a_count`,
    `nasequenceimp`.`c_count` AS `c_count`,
    `nasequenceimp`.`g_count` AS `g_count`,
    `nasequenceimp`.`t_count` AS `t_count`,
    `nasequenceimp`.`other_count` AS `other_count`,
    `nasequenceimp`.`description` AS `description`,
    `nasequenceimp`.`string4` AS `chromosome`,
    `nasequenceimp`.`nsint1` AS `chromosome_order_num`,
    `nasequenceimp`.`subclass_view` AS `subclass_view`,
    `nasequenceimp`.`modification_date` AS `modification_date`
from `nasequenceimp`;


-- --------------------------------------------------------

--
-- Structure for view `genefeature`
--
DROP TABLE IF EXISTS `genefeature`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `genefeature` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_id`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_id`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_id`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_id`,
    `nafeatureimp`.`source_ID` AS `source_id`,
    `nafeatureimp`.`external_database_ID` AS `external_database_id`,
    `nafeatureimp`.`prediction_algorithm_ID` AS `prediction_algorithm_id`,
    `nafeatureimp`.`is_predicted` AS `is_predicted`,
    `nafeatureimp`.`review_status_ID` AS `review_status_id`,
    `nafeatureimp`.`string14` AS `GENE_TYPE`,
    `nafeatureimp`.`tinyint2` AS `CONFIRMED_BY_SIMILARITY`,
    `nafeatureimp`.`nfint1` AS `PREDICTION_NUMBER`,
    `nafeatureimp`.`nfint2` AS `NUMBER_OF_EXONS`,
    `nafeatureimp`.`tinyint3` AS `HAS_INITIAL_EXON`,
    `nafeatureimp`.`tinyint4` AS `HAS_FINAL_EXON`,
    `nafeatureimp`.`float1` AS `SCORE`,
    `nafeatureimp`.`float2` AS `SECONDARY_SCORE`,
    `nafeatureimp`.`tinyint5` AS `IS_PSEUDO`,
    `nafeatureimp`.`tinyint6` AS `IS_PARTIAL`,
    `nafeatureimp`.`string1` AS `ALLELE`,
    `nafeatureimp`.`string2` AS `CITATION`,
    `nafeatureimp`.`string3` AS `EVIDENCE`,
    `nafeatureimp`.`string4` AS `gene_FUNCTION`,
    `nafeatureimp`.`string5` AS `GENE`,
    `nafeatureimp`.`string6` AS `LABEL`,
    `nafeatureimp`.`string7` AS `MAP`,
    `nafeatureimp`.`string9` AS `PHENOTYPE`,
    `nafeatureimp`.`string10` AS `PRODUCT`,
    `nafeatureimp`.`string12` AS `STANDARD_NAME`,
    `nafeatureimp`.`string13` AS `USEDIN`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'genefeature');

-- --------------------------------------------------------

--
-- Structure for view `GO`
--
DROP TABLE IF EXISTS `GO`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `GO` AS
select
    `proteininstancefeature`.`protein_instance_feature_ID` AS `protein_instance_feature_id`,
    `proteininstancefeature`.`protein_instance_id` AS `protein_instance_id`,
    `proteininstancefeature`.`feature_name` AS `feature_name`,
    `proteininstancefeature`.`subclass_view` AS `subclass_view`,
    `proteininstancefeature`.`location_start` AS `location_start`,
    `proteininstancefeature`.`location_stop` AS `location_stop`,
    `proteininstancefeature`.`length` AS `length`,
    `proteininstancefeature`.`pval_mant` AS `pval_mant`,
    `proteininstancefeature`.`pval_exp` AS `pval_exp`,
    `proteininstancefeature`.`bit_score` AS `bit_score`,
    `proteininstancefeature`.`domain_name` AS `domain_name`,
    `proteininstancefeature`.`go_id` AS `go_id`,
    `proteininstancefeature`.`prediction_id` AS `prediction_id`,
    `proteininstancefeature`.`modification_date` AS `modification_date`
from `proteininstancefeature`
where (`proteininstancefeature`.`subclass_view` = 'GO');

-- --------------------------------------------------------


-- --------------------------------------------------------

--
-- Structure for view `HmmPfam`
--
DROP TABLE IF EXISTS `HmmPfam`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `HmmPfam` AS
select
    `proteininstancefeature`.`protein_instance_feature_ID` AS `protein_instance_feature_id`,
    `proteininstancefeature`.`protein_instance_id` AS `protein_instance_id`,
    `proteininstancefeature`.`feature_name` AS `feature_name`,
    `proteininstancefeature`.`subclass_view` AS `subclass_view`,
    `proteininstancefeature`.`location_start` AS `location_start`,
    `proteininstancefeature`.`location_stop` AS `location_stop`,
    `proteininstancefeature`.`length` AS `length`,
    `proteininstancefeature`.`pval_mant` AS `pval_mant`,
    `proteininstancefeature`.`pval_exp` AS `pval_exp`,
    `proteininstancefeature`.`bit_score` AS `bit_score`,
    `proteininstancefeature`.`domain_name` AS `domain_name`,
    `proteininstancefeature`.`prediction_id` AS `prediction_id`,
    `proteininstancefeature`.`modification_date` AS `modification_date`
from `proteininstancefeature`
where (`proteininstancefeature`.`subclass_view` = 'HmmPfam');


-- --------------------------------------------------------

--
-- Structure for view `nafeature`
--
DROP TABLE IF EXISTS `nafeature`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `nafeature` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_id`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_id`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_id`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_id`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp` WITH CASCADED CHECK OPTION;

-- --------------------------------------------------------

--
-- Structure for view `nasequence`
--
DROP TABLE IF EXISTS `nasequence`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `nasequence` AS
select
    `nasequenceimp`.`na_sequence_ID` AS `na_sequence_ID`,
    `nasequenceimp`.`sequence_version` AS `sequence_version`,
    `nasequenceimp`.`subclass_view` AS `subclass_view`,
    `nasequenceimp`.`sequence_type_ID` AS `sequence_type_ID`,
    `nasequenceimp`.`taxon_ID` AS `taxon_ID`,
    `nasequenceimp`.`sequence` AS `sequence`,
    `nasequenceimp`.`length` AS `length`,
    `nasequenceimp`.`a_count` AS `a_count`,
    `nasequenceimp`.`c_count` AS `c_count`,
    `nasequenceimp`.`g_count` AS `g_count`,
    `nasequenceimp`.`t_count` AS `t_count`,
    `nasequenceimp`.`other_count` AS `other_count`,
    `nasequenceimp`.`description` AS `description`,
    `nasequenceimp`.`modification_date` AS `modification_date`
from `nasequenceimp`;

-- --------------------------------------------------------

--
-- Structure for view `ncRNA`
--
DROP TABLE IF EXISTS `ncRNA`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ncRNA` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_ID`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_ID`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_ID`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_ID`,
    `nafeatureimp`.`string1` AS `CITATION`,
    `nafeatureimp`.`string2` AS `EVIDENCE`,
    `nafeatureimp`.`string3` AS `FUNCTION`,
    `nafeatureimp`.`string4` AS `GENE`,
    `nafeatureimp`.`string5` AS `LABEL`,
    `nafeatureimp`.`string6` AS `MAP`,
    `nafeatureimp`.`string7` AS `PARTIAL`,
    `nafeatureimp`.`string8` AS `RPT_FAMILY`,
    `nafeatureimp`.`string9` AS `RPT_TYPE`,
    `nafeatureimp`.`string10` AS `RPT_UNIT`,
    `nafeatureimp`.`string11` AS `STANDARD_NAME`,
    `nafeatureimp`.`string12` AS `USEDIN`,
    `nafeatureimp`.`tinyint1` AS `IS_PARTIAL`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'ncRNA');

-- --------------------------------------------------------

--
-- Structure for view `polyA`
--
DROP TABLE IF EXISTS `polyA`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `polyA` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_ID`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_ID`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_ID`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_ID`,
    `nafeatureimp`.`string1` AS `CITATION`,
    `nafeatureimp`.`string2` AS `EVIDENCE`,
    `nafeatureimp`.`string3` AS `FUNCTION`,
    `nafeatureimp`.`string4` AS `GENE`,
    `nafeatureimp`.`string5` AS `LABEL`,
    `nafeatureimp`.`string6` AS `MAP`,
    `nafeatureimp`.`string7` AS `PARTIAL`,
    `nafeatureimp`.`string8` AS `RPT_FAMILY`,
    `nafeatureimp`.`string9` AS `RPT_TYPE`,
    `nafeatureimp`.`string10` AS `RPT_UNIT`,
    `nafeatureimp`.`string11` AS `STANDARD_NAME`,
    `nafeatureimp`.`string12` AS `USEDIN`,
    `nafeatureimp`.`tinyint1` AS `IS_PARTIAL`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'polyA');

-- --------------------------------------------------------

--
-- Structure for view `ProfileScan`
--
DROP TABLE IF EXISTS `ProfileScan`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ProfileScan` AS
select
    `proteininstancefeature`.`protein_instance_feature_ID` AS `protein_instance_feature_id`,
    `proteininstancefeature`.`protein_instance_id` AS `protein_instance_id`,
    `proteininstancefeature`.`feature_name` AS `feature_name`,
    `proteininstancefeature`.`subclass_view` AS `subclass_view`,
    `proteininstancefeature`.`location_start` AS `location_start`,
    `proteininstancefeature`.`location_stop` AS `location_stop`,
    `proteininstancefeature`.`length` AS `length`,
    `proteininstancefeature`.`pval_mant` AS `pval_mant`,
    `proteininstancefeature`.`pval_exp` AS `pval_exp`,
    `proteininstancefeature`.`bit_score` AS `bit_score`,
    `proteininstancefeature`.`domain_name` AS `domain_name`,
    `proteininstancefeature`.`prediction_id` AS `prediction_id`,
    `proteininstancefeature`.`modification_date` AS `modification_date`
from `proteininstancefeature`
where (`proteininstancefeature`.`subclass_view` = 'ProfileScan');

-- --------------------------------------------------------

--
-- Structure for view `promoter`
--
DROP TABLE IF EXISTS `promoter`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `promoter` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_ID`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_ID`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_ID`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_ID`,
    `nafeatureimp`.`string1` AS `CITATION`,
    `nafeatureimp`.`string2` AS `EVIDENCE`,
    `nafeatureimp`.`string3` AS `FUNCTION`,
    `nafeatureimp`.`string4` AS `GENE`,
    `nafeatureimp`.`string5` AS `LABEL`,
    `nafeatureimp`.`string6` AS `MAP`,
    `nafeatureimp`.`string7` AS `PARTIAL`,
    `nafeatureimp`.`string8` AS `RPT_FAMILY`,
    `nafeatureimp`.`string9` AS `RPT_TYPE`,
    `nafeatureimp`.`string10` AS `RPT_UNIT`,
    `nafeatureimp`.`string11` AS `STANDARD_NAME`,
    `nafeatureimp`.`string12` AS `USEDIN`,
    `nafeatureimp`.`tinyint1` AS `IS_PARTIAL`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'promoter');

-- --------------------------------------------------------

--
-- Structure for view `repeats`
--
DROP TABLE IF EXISTS `repeats`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `repeats` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_ID`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_ID`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_ID`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_ID`,
    `nafeatureimp`.`string1` AS `CITATION`,
    `nafeatureimp`.`string2` AS `EVIDENCE`,
    `nafeatureimp`.`string3` AS `FUNCTION`,
    `nafeatureimp`.`string4` AS `GENE`,
    `nafeatureimp`.`string5` AS `LABEL`,
    `nafeatureimp`.`string6` AS `MAP`,
    `nafeatureimp`.`string7` AS `PARTIAL`,
    `nafeatureimp`.`string8` AS `RPT_FAMILY`,
    `nafeatureimp`.`string9` AS `RPT_TYPE`,
    `nafeatureimp`.`string10` AS `RPT_UNIT`,
    `nafeatureimp`.`string11` AS `STANDARD_NAME`,
    `nafeatureimp`.`string12` AS `USEDIN`,
    `nafeatureimp`.`tinyint1` AS `IS_PARTIAL`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'REPEAT');

-- --------------------------------------------------------

--
-- Structure for view `rnatype`
--
DROP TABLE IF EXISTS `rnatype`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `rnatype` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_id`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_id`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_id`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_id`,
    `nafeatureimp`.`string1` AS `ANTICODON`,
    `nafeatureimp`.`string2` AS `CITATION`,
    `nafeatureimp`.`string3` AS `CODON`,
    `nafeatureimp`.`string4` AS `EVIDENCE`,
    `nafeatureimp`.`string5` AS `FUNCTION`,
    `nafeatureimp`.`string6` AS `GENE`,
    `nafeatureimp`.`string7` AS `LABEL`,
    `nafeatureimp`.`string8` AS `MAP`,
    `nafeatureimp`.`string9` AS `PARTIAL`,
    `nafeatureimp`.`string10` AS `PRODUCT`,
    `nafeatureimp`.`string11` AS `PSEUDO`,
    `nafeatureimp`.`string12` AS `STANDARD_NAME`,
    `nafeatureimp`.`string13` AS `USEDIN`,
    `nafeatureimp`.`tinyint1` AS `IS_PARTIAL`,
    `nafeatureimp`.`tinyint2` AS `IS_PSEUDO`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'rnatype');

-- --------------------------------------------------------

--
-- Structure for view `ScanRegExp`
--
DROP TABLE IF EXISTS `ScanRegExp`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ScanRegExp` AS
select
    `proteininstancefeature`.`protein_instance_feature_ID` AS `protein_instance_feature_id`,
    `proteininstancefeature`.`protein_instance_id` AS `protein_instance_id`,
    `proteininstancefeature`.`feature_name` AS `feature_name`,
    `proteininstancefeature`.`subclass_view` AS `subclass_view`,
    `proteininstancefeature`.`location_start` AS `location_start`,
    `proteininstancefeature`.`location_stop` AS `location_stop`,
    `proteininstancefeature`.`length` AS `length`,
    `proteininstancefeature`.`pval_mant` AS `pval_mant`,
    `proteininstancefeature`.`pval_exp` AS `pval_exp`,
    `proteininstancefeature`.`bit_score` AS `bit_score`,
    `proteininstancefeature`.`domain_name` AS `domain_name`,
    `proteininstancefeature`.`prediction_id` AS `prediction_id`,
    `proteininstancefeature`.`modification_date` AS `modification_date`
from `proteininstancefeature`
where (`proteininstancefeature`.`subclass_view` = 'ScanRegExp');

-- --------------------------------------------------------

--
-- Structure for view `Seg`
--
DROP TABLE IF EXISTS `Seg`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `Seg` AS
select
    `proteininstancefeature`.`protein_instance_feature_ID` AS `protein_instance_feature_id`,
    `proteininstancefeature`.`protein_instance_id` AS `protein_instance_id`,
    `proteininstancefeature`.`feature_name` AS `feature_name`,
    `proteininstancefeature`.`subclass_view` AS `subclass_view`,
    `proteininstancefeature`.`location_start` AS `location_start`,
    `proteininstancefeature`.`location_stop` AS `location_stop`,
    `proteininstancefeature`.`length` AS `length`,
    `proteininstancefeature`.`pval_mant` AS `pval_mant`,
    `proteininstancefeature`.`pval_exp` AS `pval_exp`,
    `proteininstancefeature`.`bit_score` AS `bit_score`,
    `proteininstancefeature`.`domain_name` AS `domain_name`,
    `proteininstancefeature`.`prediction_id` AS `prediction_id`,
    `proteininstancefeature`.`modification_date` AS `modification_date`
from `proteininstancefeature`
where (`proteininstancefeature`.`subclass_view` = 'Seg');

-- --------------------------------------------------------

--
-- Structure for view `seqvariation`
--
DROP TABLE IF EXISTS `seqvariation`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `seqvariation` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_id`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_id`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_id`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_id`,
    `nafeatureimp`.`string1` AS `CITATION`,
    `nafeatureimp`.`string2` AS `CLONE`,
    `nafeatureimp`.`string3` AS `EVIDENCE`,
    `nafeatureimp`.`string5` AS `FUNCTION`,
    `nafeatureimp`.`string6` AS `GENE`,
    `nafeatureimp`.`string7` AS `LABEL`,
    `nafeatureimp`.`string8` AS `MAP`,
    `nafeatureimp`.`string9` AS `ORGANISM`,
    `nafeatureimp`.`string4` AS `STRAIN`,
    `nafeatureimp`.`string10` AS `PARTIAL`,
    `nafeatureimp`.`string11` AS `PHENOTYPE`,
    `nafeatureimp`.`string12` AS `PRODUCT`,
    `nafeatureimp`.`string13` AS `STANDARD_NAME`,
    `nafeatureimp`.`string20` AS `SUBSTITUTE`,
    `nafeatureimp`.`string15` AS `NUM`,
    `nafeatureimp`.`string16` AS `USEDIN`,
    `nafeatureimp`.`string17` AS `MOD_BASE`,
    `nafeatureimp`.`tinyint1` AS `IS_PARTIAL`,
    `nafeatureimp`.`float1` AS `FREQUENCY`,
    `nafeatureimp`.`string18` AS `ALLELE`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'seqvariation');

-- --------------------------------------------------------

--
-- Structure for view `SOURCE`
--
DROP TABLE IF EXISTS `SOURCE`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `SOURCE` AS
select `nafeatureimp`.`na_feature_ID` AS `na_feature_id`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_id`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_id`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_id`,
    `nafeatureimp`.`string1` AS `CELL_LINE`,
    `nafeatureimp`.`string2` AS `CELL_TYPE`,
    `nafeatureimp`.`string3` AS `CHROMOPLAST`,
    `nafeatureimp`.`string4` AS `CHROMOSOME`,
    `nafeatureimp`.`string5` AS `CLONE`,
    `nafeatureimp`.`string6` AS `CLONE_LIB`,
    `nafeatureimp`.`string7` AS `CULTIVAR`,
    `nafeatureimp`.`string8` AS `CYANELLE`,
    `nafeatureimp`.`string9` AS `DEV_STAGE`,
    `nafeatureimp`.`string10` AS `FOCUS`,
    `nafeatureimp`.`string11` AS `FREQUENCY`,
    `nafeatureimp`.`string12` AS `GERMLINE`,
    `nafeatureimp`.`string13` AS `HAPLOTYPE`,
    `nafeatureimp`.`text1` AS `INSERTION_SEQ`,
    `nafeatureimp`.`string14` AS `ISOLATE`,
    `nafeatureimp`.`string15` AS `KINETOPLAST`,
    `nafeatureimp`.`string16` AS `LAB_HOST`,
    `nafeatureimp`.`string17` AS `MACRONUCLEAR`,
    `nafeatureimp`.`string18` AS `ORGANELLE`,
    `nafeatureimp`.`string19` AS `POP_VARIANT`,
    `nafeatureimp`.`string20` AS `PLASMID`,
    `nafeatureimp`.`string21` AS `PROVIRAL`,
    `nafeatureimp`.`string22` AS `REARRANGED`,
    `nafeatureimp`.`string23` AS `SEQUENCED_MOL`,
    `nafeatureimp`.`string24` AS `SEROTYPE`,
    `nafeatureimp`.`string25` AS `SEX`,
    `nafeatureimp`.`string26` AS `SPECIFIC_HOST`,
    `nafeatureimp`.`string27` AS `STRAIN`,
    `nafeatureimp`.`string28` AS `SUB_CLONE`,
    `nafeatureimp`.`string29` AS `SUB_SPECIES`,
    `nafeatureimp`.`string30` AS `SUB_STRAIN`,
    `nafeatureimp`.`string31` AS `TISSUE_LIB`,
    `nafeatureimp`.`string32` AS `TRANSPOSON`,
    `nafeatureimp`.`string33` AS `VARIETY`,
    `nafeatureimp`.`string34` AS `VIRION`,
    `nafeatureimp`.`string35` AS `CHLOROPLAST`,
    `nafeatureimp`.`string36` AS `CITATION`,
    `nafeatureimp`.`string37` AS `MAP`,
    `nafeatureimp`.`string38` AS `ORGANISM`,
    `nafeatureimp`.`string39` AS `SPECIMEN_VOUCHER`,
    `nafeatureimp`.`string40` AS `TISSUE_TYPE`,
    `nafeatureimp`.`string41` AS `USEDIN`,
    `nafeatureimp`.`string42` AS `LABEL`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'source');

-- --------------------------------------------------------

--
-- Structure for view `SuperFamily`
--
DROP TABLE IF EXISTS `SuperFamily`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `SuperFamily` AS
select
    `proteininstancefeature`.`protein_instance_feature_ID` AS `protein_instance_feature_id`,
    `proteininstancefeature`.`protein_instance_id` AS `protein_instance_id`,
    `proteininstancefeature`.`feature_name` AS `feature_name`,
    `proteininstancefeature`.`subclass_view` AS `subclass_view`,
    `proteininstancefeature`.`location_start` AS `location_start`,
    `proteininstancefeature`.`location_stop` AS `location_stop`,
    `proteininstancefeature`.`length` AS `length`,
    `proteininstancefeature`.`pval_mant` AS `pval_mant`,
    `proteininstancefeature`.`pval_exp` AS `pval_exp`,
    `proteininstancefeature`.`bit_score` AS `bit_score`,
    `proteininstancefeature`.`domain_name` AS `domain_name`,
    `proteininstancefeature`.`prediction_id` AS `prediction_id`,
    `proteininstancefeature`.`modification_date` AS `modification_date`
from `proteininstancefeature`
where (`proteininstancefeature`.`subclass_view` = 'SuperFamily');

-- --------------------------------------------------------


--
-- Structure for view `transcript`
--
DROP TABLE IF EXISTS `transcript`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `transcript` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_id`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_id`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_id`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_id`,
    `nafeatureimp`.`string1` AS `CITATION`,
    `nafeatureimp`.`string2` AS `CLONE`,
    `nafeatureimp`.`string3` AS `CODON`,
    `nafeatureimp`.`nfint1` AS `CODON_START`,
    `nafeatureimp`.`string4` AS `CONS_SPLICE`,
    `nafeatureimp`.`string5` AS `EC_NUMBER`,
    `nafeatureimp`.`string6` AS `EVIDENCE`,
    `nafeatureimp`.`string7` AS `transcript_FUNCTION`,
    `nafeatureimp`.`string8` AS `GENE`,
    `nafeatureimp`.`string9` AS `KO_ID`,
    `nafeatureimp`.`string10` AS `MAP`,
    `nafeatureimp`.`string11` AS `NUM`,
    `nafeatureimp`.`string12` AS `PARTIAL`,
    `nafeatureimp`.`string13` AS `PRODUCT`,
    `nafeatureimp`.`string14` AS `PROTEIN_ID`,
    `nafeatureimp`.`string15` AS `PSEUDO`,
    `nafeatureimp`.`string16` AS `STANDARD_NAME`,
    `nafeatureimp`.`text1` AS `TRANSLATION`,
    `nafeatureimp`.`string17` AS `TRANSL_EXCEPT`,
    `nafeatureimp`.`nfint2` AS `TRANSL_TABLE`,
    `nafeatureimp`.`string18` AS `USEDIN`,
    `nafeatureimp`.`tinyint1` AS `IS_PARTIAL`,
    `nafeatureimp`.`tinyint2` AS `IS_PSEUDO`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (subclass_view = 'Transcript' or subclass_view = 'mRNA');

-- --------------------------------------------------------

--
-- Structure for view `tRNA`
--
DROP TABLE IF EXISTS `tRNA`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `tRNA` AS
select
    `nafeatureimp`.`na_feature_ID` AS `na_feature_ID`,
    `nafeatureimp`.`na_sequence_ID` AS `na_sequence_ID`,
    `nafeatureimp`.`subclass_view` AS `subclass_view`,
    `nafeatureimp`.`sequence_ontology_ID` AS `sequence_ontology_ID`,
    `nafeatureimp`.`name` AS `name`,
    `nafeatureimp`.`parent_ID` AS `parent_ID`,
    `nafeatureimp`.`string1` AS `CITATION`,
    `nafeatureimp`.`string2` AS `EVIDENCE`,
    `nafeatureimp`.`string3` AS `FUNCTION`,
    `nafeatureimp`.`string4` AS `GENE`,
    `nafeatureimp`.`string5` AS `LABEL`,
    `nafeatureimp`.`string6` AS `MAP`,
    `nafeatureimp`.`string7` AS `PARTIAL`,
    `nafeatureimp`.`string8` AS `RPT_FAMILY`,
    `nafeatureimp`.`string9` AS `RPT_TYPE`,
    `nafeatureimp`.`string10` AS `RPT_UNIT`,
    `nafeatureimp`.`string11` AS `STANDARD_NAME`,
    `nafeatureimp`.`string12` AS `USEDIN`,
    `nafeatureimp`.`tinyint1` AS `IS_PARTIAL`,
    `nafeatureimp`.`modification_date` AS `modification_date`
from `nafeatureimp`
where (`nafeatureimp`.`subclass_view` = 'tRNA');
