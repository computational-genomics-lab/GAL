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
  PRIMARY KEY (`user_ID`),
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


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
  FOREIGN KEY(`user_ID`) REFERENCES userinfo(`user_ID`),

) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `databaseinfo`;
CREATE TABLE `databaseinfo` (
  `database_ID` int(11) NOT NULL AUTO_INCREMENT,
  `version` varchar(10) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `description` varchar(500) NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`database_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `tableinfo`;
CREATE TABLE `tableinfo` (
  `table_ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `table_type` varchar(50) NOT NULL,
  `primary_key_column` varchar(50) DEFAULT NULL,
  `database_ID` int(11) NOT NULL,
  `is_versioned` tinyint(1) NOT NULL,
  `is_view` tinyint(1) NOT NULL,
  `view_on_table_ID` int(11) DEFAULT NULL,
  `superclass_table_ID` int(11) DEFAULT NULL,
  `is_updatable` tinyint(1) NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`table_ID`),
  FOREIGN KEY (`database_ID`) REFERENCES `databaseinfo` (`database_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




--
-- SRES Schema; Shared resources
--

DROP TABLE IF EXISTS `Organism`;
CREATE TABLE IF NOT EXISTS `Organism`(
    ORGANISM_ID INT(11) NOT NULL AUTO_INCREMENT,
    TAXON_ID INT(11) NOT NULL,
    TAXON_NAME VARCHAR(100) NOT NULL,
    SPECIES VARCHAR(100) NOT NULL,
    STRAIN VARCHAR(100) NULL,
    PHYLUM VARCHAR(100) NULL,
    FAMILY VARCHAR(100) NULL,
    GENUS VARCHAR(100) NULL,
    ORDERS VARCHAR(100) NULL,
    CLASS varchar(100) NULL,
    SUPERKINGDOM VARCHAR(100) NULL,
    VERSION FLOAT NOT NULL DEFAULT 1,
    NEW_VERSION FLOAT NULL,
    COMMENT VARCHAR(100) NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (ORGANISM_ID)
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
  `go_evidence_code_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `modification_date` varchar(50) NOT NULL,
  PRIMARY KEY (`go_evidence_code_id`)
) ENGINE=InnoDB AUTO_INCREMENT=48939 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `log_ID` int(11) NOT NULL AUTO_INCREMENT,
  `user_ID` varchar(50) NOT NULL,
  `organism_id` varchar(100) NOT NULL,
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
CREATE TABLE `taxon` (
  `taxon_ID` int(11) NOT NULL AUTO_INCREMENT,
  `ncbi_taxon_ID` int(11) DEFAULT NULL,
  `parent_ID` int(11) DEFAULT NULL,
  `taxon_name` varchar(255) NOT NULL,
  `taxon_strain` varchar(255) NOT NULL,
  `rank` varchar(255) NOT NULL,
  `geneticcode_ID` int(11) DEFAULT NULL,
  `mitochondrial_geneticcode_ID` int(11) DEFAULT NULL,
  `modification_date` varchar(50) NOT NULL,
  PRIMARY KEY (`taxon_ID`),
  FOREIGN KEY (`geneticcode_ID`) REFERENCES geneticcode(`geneticcode_ID`),
  FOREIGN KEY (`mitochondrial_geneticcode_ID`) REFERENCES geneticcode(`geneticcode_ID`)
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

--
-- Dots Schema ; It has tables and views
--

--
-- Tables
--

DROP TABLE IF EXISTS `sequencetype`;
CREATE TABLE `sequencetype` (
  `sequence_type_ID` int(11) NOT NULL AUTO_INCREMENT,
  `neucleotide_ID` int(11) NOT NULL,
  `sub_type` int(11) DEFAULT NULL,
  `strand` varchar(10) DEFAULT NULL,
  `hierarchy` int(5) NOT NULL,
  `parent_sequence_type_ID` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sequence_type_ID`),
  KEY `SEQUENCETYPE_FK` (`parent_sequence_type_ID`),
  CONSTRAINT `SEQUENCETYPE_FK` FOREIGN KEY (`parent_sequence_type_ID`) REFERENCES `sequencetype` (`sequence_type_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


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
CREATE TABLE `nafeatureimp` (
  `na_feature_ID` int(11) NOT NULL AUTO_INCREMENT,
  `na_sequence_ID` int(11) DEFAULT NULL,
  `subclass_view` varchar(50) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `sequence_ontology_ID` int(11) DEFAULT NULL,
  `parent_ID` int(11) DEFAULT NULL,
  `external_database_ID` int(11) DEFAULT NULL,
  `source_ID` int(11) DEFAULT NULL,
  `prediction_algorithm_ID` int(11) DEFAULT NULL,
  `is_predicted` tinyint(1) DEFAULT NULL,
  `review_status_ID` int(11) DEFAULT NULL,
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
  `text1` text,
  `string1` varchar(1000) DEFAULT NULL,
  `string2` varchar(255) DEFAULT NULL,
  `string3` varchar(255) DEFAULT NULL,
  `string4` varchar(255) DEFAULT NULL,
  `string5` varchar(2000) DEFAULT NULL,
  `string6` varchar(255) DEFAULT NULL,
  `string7` varchar(255) DEFAULT NULL,
  `string8` varchar(255) DEFAULT NULL,
  `string9` varchar(1000) DEFAULT NULL,
  `string10` varchar(255) DEFAULT NULL,
  `string11` varchar(255) DEFAULT NULL,
  `string12` varchar(255) DEFAULT NULL,
  `string13` varchar(1000) DEFAULT NULL,
  `string14` varchar(500) DEFAULT NULL,
  `string15` varchar(255) DEFAULT NULL,
  `string16` varchar(255) DEFAULT NULL,
  `string17` varchar(255) DEFAULT NULL,
  `string18` varchar(255) DEFAULT NULL,
  `string19` varchar(255) DEFAULT NULL,
  `string20` varchar(4000) DEFAULT NULL,
  `string21` varchar(255) DEFAULT NULL,
  `string22` varchar(255) DEFAULT NULL,
  `string23` varchar(255) DEFAULT NULL,
  `string24` varchar(255) DEFAULT NULL,
  `string25` varchar(255) DEFAULT NULL,
  `string26` varchar(255) DEFAULT NULL,
  `string27` varchar(255) DEFAULT NULL,
  `string28` varchar(255) DEFAULT NULL,
  `string29` varchar(255) DEFAULT NULL,
  `string30` varchar(255) DEFAULT NULL,
  `string31` varchar(255) DEFAULT NULL,
  `string32` varchar(255) DEFAULT NULL,
  `string33` varchar(255) DEFAULT NULL,
  `string34` varchar(255) DEFAULT NULL,
  `string35` varchar(255) DEFAULT NULL,
  `string36` varchar(255) DEFAULT NULL,
  `string37` varchar(255) DEFAULT NULL,
  `string38` varchar(255) DEFAULT NULL,
  `string39` varchar(255) DEFAULT NULL,
  `string40` varchar(255) DEFAULT NULL,
  `string41` varchar(255) DEFAULT NULL,
  `string42` varchar(255) DEFAULT NULL,
  `string43` varchar(255) DEFAULT NULL,
  `string44` varchar(255) DEFAULT NULL,
  `string45` varchar(255) DEFAULT NULL,
  `string46` varchar(255) DEFAULT NULL,
  `string47` varchar(255) DEFAULT NULL,
  `string48` varchar(255) DEFAULT NULL,
  `string49` varchar(255) DEFAULT NULL,
  `string50` varchar(255) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`na_feature_ID`),
  KEY `nafeatureimp_FK02` (`na_sequence_ID`),
  KEY `nafeatureimp_FK03` (`external_database_ID`),
  KEY `nafeatureimp_FK05` (`prediction_algorithm_ID`),
  KEY `nafeatureimp_FK01` (`parent_ID`),
  CONSTRAINT `nafeatureimp_FK03` FOREIGN KEY (`na_sequence_ID`) REFERENCES `nasequenceimp` (`na_sequence_ID`),
  CONSTRAINT `nafeatureimp_FK01` FOREIGN KEY (`parent_ID`) REFERENCES `nasequenceimp` (`na_sequence_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `nalocation`;
CREATE TABLE `nalocation` (
  `na_location_ID` int(11) NOT NULL AUTO_INCREMENT,
  `na_feature_ID` int(11) NOT NULL,
  `start_min` int(12) DEFAULT NULL,
  `start_max` int(12) DEFAULT NULL,
  `end_min` int(12) DEFAULT NULL,
  `end_max` int(12) DEFAULT NULL,
  `loc_order` int(12) DEFAULT NULL,
  `is_reversed` int(3) DEFAULT NULL,
  `is_excluded` int(3) DEFAULT NULL,
  `db_name` varchar(100) DEFAULT NULL,
  `db_identifier` varchar(25) DEFAULT NULL,
  `literal_sequence` varchar(255) DEFAULT NULL,
  `location_type` varchar(50) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `debug_field` varchar(4000) DEFAULT NULL,
  `modification_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`na_location_ID`),
  KEY `nalocation_FK04` (`na_feature_ID`),
  CONSTRAINT `nalocation_FK04` FOREIGN KEY (`na_feature_ID`) REFERENCES `nafeatureimp` (`na_feature_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

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
CREATE TABLE `geneinstance` (
  `gene_instance_id` int(11) NOT NULL,
  `gene_instance_category_id` int(3) NOT NULL,
  `gene_id` int(10) NOT NULL,
  `na_feature_ID` int(10) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `reviewer_summary` varchar(4000) DEFAULT NULL,
  `is_reference` int(1) NOT NULL,
  `review_status_id` int(10) NOT NULL,
  `modification_date` date NOT NULL,
  PRIMARY KEY (`gene_instance_id`),
  KEY `geneinstance_fk05` (`review_status_id`),
  KEY `geneinstance_fk06` (`gene_id`),
  KEY `geneinstance_fk07` (`na_feature_ID`),
  KEY `geneinstance_fk08` (`gene_instance_category_id`),
  CONSTRAINT `geneinstance_fk07` FOREIGN KEY (`na_feature_ID`) REFERENCES `nafeatureimp` (`na_feature_ID`),
  CONSTRAINT `geneinstance_fk06` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`gene_ID`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  `pathway_id` int(11) NOT NULL AUTO_INCREMENT,
  `taxon_id` int(11) NOT NULL,
  `version` float NOT NULL,
  `url` text NOT NULL,
  PRIMARY KEY (`pathway_id`)
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
CREATE TABLE `protein` (
  `protein_ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `rna_ID` int(11) NOT NULL,
  `review_status_ID` int(11) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `reviewer_summary` varchar(4000) DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`protein_ID`),
  KEY `protein_FK01` (`rna_ID`),
  KEY `protein_FK02` (`review_status_ID`),
  CONSTRAINT `protein_FK01` FOREIGN KEY (`rna_ID`) REFERENCES `rna` (`rna_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `protein_cluster`;
CREATE TABLE `protein_cluster` (
  `protein_cluster_id` int(11) NOT NULL AUTO_INCREMENT,
  `cluster_id` int(11) NOT NULL,
  `gene_id` int(11) NOT NULL,
  `taxon_id` int(11) NOT NULL,
  `desc` varchar(100) NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`protein_cluster_id`)
) ENGINE=InnoDB AUTO_INCREMENT=45475 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `proteininstancefeature`;
CREATE TABLE `proteininstancefeature` (
  `protein_instance_feature_ID` int(11) NOT NULL AUTO_INCREMENT,
  `protein_instance_id` int(11) NOT NULL,
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
  KEY `proteininstancefeature_FK01` (`protein_instance_id`),
  KEY `proteininstancefeature_FK02` (`prediction_algorithm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1942002 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `signalP`;
CREATE TABLE `signalP` (
  `signalp_ID` int(11) NOT NULL AUTO_INCREMENT,
  `gene_ID` varchar(100) NOT NULL,
  `taxon_ID` int(11) NOT NULL,
  `Y-score` float DEFAULT NULL,
  `D-score` float DEFAULT NULL,
  `Y-pos` int(11) DEFAULT NULL,
  `C-score` float NOT NULL,
  `S-score` float NOT NULL,
  `cleavage_site` varchar(50) NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`signalp_ID`),
  FOREIGN KEY (`gene_ID`) REFERENCES `gene` (`gene_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `PSORT`;
CREATE TABLE `PSORT` (
  `psort_ID` int(11) NOT NULL AUTO_INCREMENT,
  `gene_ID` varchar(100) NOT NULL,
  `taxon_ID` int(11) NOT NULL,
  `type` varchar(60) DEFAULT NULL,
  `score` float DEFAULT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`psort_ID`),
  FOREIGN KEY (`gene_ID`) REFERENCES `gene` (`gene_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=138156 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `SECRETOME`;
CREATE TABLE `SECRETOME` (
  `secretome_ID` int(11) NOT NULL AUTO_INCREMENT,
  `gene_ID` varchar(100) NOT NULL,
  `taxon_ID` int(11) NOT NULL,
  `NN-score` float NOT NULL,
  `odds` float NOT NULL,
  `weighted_score` float NOT NULL,
  `modification_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`secretome_ID`),
  FOREIGN KEY (`gene_ID`) REFERENCES `gene` (`gene_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=124402 DEFAULT CHARSET=latin1;

-- Views



