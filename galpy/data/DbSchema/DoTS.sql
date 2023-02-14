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
	PRIMARY KEY (ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `SequenceType`;
CREATE TABLE IF NOT EXISTS `SequenceType`(
    SEQUENCE_TYPE_ID INT(11) NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(50) NOT NULL,
    DESCRIPTION VARCHAR(255) NULL,
    PARENT_SEQUENCE_TYPE_ID INT(11) NULL,
    PRIMARY KEY (SEQUENCE_TYPE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

INSERT INTO `SequenceType` (SEQUENCE_TYPE_ID, NAME, DESCRIPTION, PARENT_SEQUENCE_TYPE_ID) VALUES
(1, 'Chromosomes', 'Finished Genome', 1),
(2, 'Scaffold', 'Draft Genome', 1),
(3, 'Genomic contif','genomics contig', 1),
(4, 'EST contig', 'Est contig', 1),
(5, 'EST', 'EST', 1),
(6, 'Transcript', 'Transcript', 1),
(7, 'Protein Sequence', 'Protein Sequence', 6);


DROP TABLE IF EXISTS `NASequenceImp`;
CREATE TABLE IF NOT EXISTS `NASequenceImp`(
    NA_SEQUENCE_ID INT(11) NOT NULL AUTO_INCREMENT,
    SEQUENCE_VERSION FLOAT NOT NULL,
    SUBCLASS_VIEW VARCHAR(50),
    SEQUENCE_TYPE_ID INT(11) NOT NULL,
    TAXON_ID INT(11),
    SEQUENCE LONGTEXT,
    LENGTH INT(11),
    A_COUNT INT(11),
    T_COUNT INT(11),
    G_COUNT INT(11),
    C_COUNT INT(11),
    OTHER_COUNT INT(11),
    DESCRIPTION VARCHAR(255),
    SOURCE_NA_SEQUENCE_ID INT(11) NULL,
    SEQUENCE_PIECE_ID INT(11) NULL,
    SEQUENCING_CENTER_CONTACT_ID INT(11) NULL,
    MODIFICATION_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    STRING1 VARCHAR(255) NULL,
    STRING2 VARCHAR(255) NULL,
    STRING3 VARCHAR(255) NULL,
    PRIMARY KEY (NA_SEQUENCE_ID),
    FOREIGN KEY (SEQUENCE_TYPE_ID) REFERENCES SequenceType(SEQUENCE_TYPE_ID),
    FOREIGN KEY (SOURCE_NA_SEQUENCE_ID) REFERENCES NASequenceImp(NA_SEQUENCE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `NAFeatureImp`;
CREATE TABLE IF NOT EXISTS `NAFeatureImp`(
    NA_FEATURE_ID INT(11) NOT NULL AUTO_INCREMENT,
    NA_SEQUENCE_ID INT(11) NOT NULL,
    SUBCLASS_VIEW VARCHAR(50),
    FEATURE_TYPE VARCHAR(50) NOT NULL,
    NAME VARCHAR(150) NULL,
    PARENT_ID INT(11) NULL,
    EXTERNAL_DATABASE_ID INT(11),
    SOURCE_ID INT(11),
    PREDICTION_ALGORITHM_ID INT(11),
    IS_PREDICTED INT(11),
    REVIEW_STATUS_ID INT(11),
    PRIMARY KEY (NA_FEATURE_ID),
    FOREIGN KEY (NA_SEQUENCE_ID) REFERENCES NASequenceImp(NA_SEQUENCE_ID),
    FOREIGN KEY (PARENT_ID) REFERENCES NAFeatureImp(NA_FEATURE_ID) ON DELETE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `NALocation`;
CREATE TABLE IF NOT EXISTS `NALocation`(
    NA_LOCATION_ID INT(11) NOT NULL AUTO_INCREMENT,
    NA_FEATURE_ID INT(11) NOT NULL,
    START_MIN INT(11),
    START_MAX INT(11),
    END_MIN INT(11),
    END_MAX INT(11),
    LOC_ORDER INT(3),
    IS_REVERSED INT(3),
    IS_EXCLUDED INT(3),
    LITERAL_SEQUENCE VARCHAR(255),
    LOCATION_TYPE VARCHAR(50),
    PRIMARY KEY(NA_LOCATION_ID),
    FOREIGN KEY(NA_FEATURE_ID) REFERENCES NAFeatureImp(NA_FEATURE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;


DROP TABLE IF EXISTS `GeneInstance`;
CREATE TABLE IF NOT EXISTS `GeneInstance`(
    GENE_INSTANCE_ID INT(11) NOT NULL AUTO_INCREMENT,
    NA_FEATURE_ID INT(11),
    DESCRIPTION VARCHAR(255),
    REVIEWER_SUMMARY VARCHAR(255),
    IS_REFERENCE INT(11),
    REVIEW_STATUS_ID INT(11),
    MODIFICATION_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (GENE_INSTANCE_ID),
    FOREIGN KEY(NA_FEATURE_ID) REFERENCES NAFeatureImp(NA_FEATURE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `Protein`;
CREATE TABLE IF NOT EXISTS `Protein`(
    PROTEIN_ID INT(11) NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(150) NOT NULL,
    DESCRIPTION VARCHAR(255),
    REVIEW_STATUS_ID INT(11),
    REVIEWER_SUMMARY VARCHAR(255),
    GENE_INSTANCE_ID INT(11),
    SEQUENCE TEXT NOT NULL,
    PRIMARY KEY (PROTEIN_ID),
    FOREIGN KEY(GENE_INSTANCE_ID) REFERENCES GeneInstance(GENE_INSTANCE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;


DROP TABLE IF EXISTS `SignalP`;
CREATE TABLE IF NOT EXISTS `SignalP`(
SIGNALP_ID INT(11) NOT NULL AUTO_INCREMENT,
GENE_INSTANCE_ID INT(11) NOT NULL,
`Y-SCORE` FLOAT NULL,
`Y-POS` INT(11) NULL,
`D-SCORE` FLOAT NULL,
STATUS varchar(20) NULL,
PRIMARY KEY(SIGNALP_ID),
FOREIGN KEY(GENE_INSTANCE_ID) REFERENCES GeneInstance(GENE_INSTANCE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `Tmhmm`;
CREATE TABLE IF NOT EXISTS `Tmhmm`(
TMHMM_ID INT(11) NOT NULL AUTO_INCREMENT,
GENE_INSTANCE_ID INT(11) NOT NULL,
INSIDE VARCHAR(60),
OUTSIDE VARCHAR(60),
TMHELIX VARCHAR(60),
MODIFICATION_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(TMHMM_ID),
FOREIGN KEY(GENE_INSTANCE_ID) REFERENCES GeneInstance(GENE_INSTANCE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

DROP TABLE IF EXISTS `HmmPfam`;
CREATE TABLE IF NOT EXISTS `HmmPfam`(
    PFAM_ID INT(11) NOT NULL AUTO_INCREMENT,
    GENE_INSTANCE_ID INT(11) NOT NULL,
    E_VALUE FLOAT,
    SCORE FLOAT,
    BIAS FLOAT,
    ACCESSION_ID VARCHAR(100),
    DOMAIN_NAME VARCHAR(1000),
    DOMAIN_DESCRIPTION VARCHAR(1000),
    MODIFICATION_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(PFAM_ID),
    FOREIGN KEY(GENE_INSTANCE_ID) REFERENCES GeneInstance(GENE_INSTANCE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;


DROP TABLE IF EXISTS `SamAlignment`;
CREATE TABLE IF NOT EXISTS `SamAlignment`(
SAM_ALIGNMENT_ID INT(11) NOT NULL AUTO_INCREMENT,
QUERY_NA_SEQUENCE_ID INT(11) NOT NULL,
TARGET_NA_SEQUENCE_ID INT(11) NOT NULL,
QUERY_TAXON_ID INT(11) NOT NULL,
QUERY_ORGANISM_VERSION FLOAT NOT NULL,
TARGET_TAXON_ID INT(11) NOT NULL,
TARGET_ORGANISM_VERSION FLOAT NOT NULL,
MATCHING_QUERY_LENGTH INT(11) NULL,
MATCHING_TARGET_LENGTH INT(11) NULL,
CIGER_STRING TEXT NOT NULL,
QUERY_START INT(11),
QUERY_END INT(11),
TARGET_START INT(11),
TARGET_END INT(11),
COUNTM INT(11),
SCORE INT(4) NULL,
EVALUE VARCHAR(50) NULL,
LENGTH INT(11),
MODIFICATION_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(SAM_ALIGNMENT_ID),
FOREIGN KEY(QUERY_NA_SEQUENCE_ID) REFERENCES NASequenceImp(NA_SEQUENCE_ID),
FOREIGN KEY(TARGET_NA_SEQUENCE_ID) REFERENCES NASequenceImp(NA_SEQUENCE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;


DROP TABLE IF EXISTS `InterProScan`;
CREATE TABLE IF NOT EXISTS `InterProScan`(
interpro_scan_ID INT(11) NOT NULL AUTO_INCREMENT,
GENE_INSTANCE_ID INT(11) NOT NULL,
FEATURE_NAME VARCHAR(255) NOT NULL,
SUBCLASS_VIEW VARCHAR(255) NULL,
LOCATION_START INT(10) NULL,
LOCATION_STOP INT(10) NULL,
LENGTH INT(10) NULL,
PREDICTION_ALGORITHM_ID INT(11) NULL,
PVAL_MANT FLOAT NULL,
PVAL_EXP INT(10) NULL,
BIT_SCORE FLOAT(20) NULL,
DOMAIN_NAME varchar(1000) NULL,
PREDICTION_ID varchar(100) NULL,
GO_ID varchar(100) NULL,
IS_REVIEWED INT(1) NULL,
ALGORITHM_ID INT(11) NULL,
MODIFICATION_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(interpro_scan_ID),
FOREIGN KEY(GENE_INSTANCE_ID) REFERENCES GeneInstance(GENE_INSTANCE_ID)
)ENGINE=InnoDB AUTO_INCREMENT = 1;

