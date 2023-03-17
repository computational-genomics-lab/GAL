# galEupy
Python module for GAL. It does the data processing.
 
## Installation
### For latest pip version
```commandline
pip install galEupy
```

### For latest development version
```commandline
pip install git+https://github.com/computational-genomics-lab/GAL.git
```
or
```batch
git clone https://github.com/computational-genomics-lab/GAL.git
cd GAL
pip install .
```

## Usage
```batch
galEupy --help

```

```batch
Welcome to galEupy
usage: galEupy [-h] [-db DBCONFIG] [-path PATHCONFIG] [-org ORGCONFIG] [-upload {all,centraldogma,proteinannotation}] [-info [INFO]] [-org_info [ORG_INFO]]
               [-remove_org [REMOVE_ORG]] [-remove_db [REMOVE_DB]] [-v {none,debug,info,warning,error,d,e,i,w}] [-log LOG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -db DBCONFIG, --dbconfig DBCONFIG
                        Database configuration file name
  -path PATHCONFIG, --pathconfig PATHCONFIG
                        path configuration file name
  -org ORGCONFIG, --orgconfig ORGCONFIG
                        Organism configuration file name
  -upload {all,centraldogma,proteinannotation}, --upload {all,centraldogma,proteinannotation}
                        Upload data using different levels
  -info [INFO], --info [INFO]
                        Gives information of the table status
  -org_info [ORG_INFO], --org_info [ORG_INFO]
                        Gives information of an organism's upload status
  -remove_org [REMOVE_ORG], --remove_org [REMOVE_ORG]
                        Removes an organism details from the database
  -remove_db [REMOVE_DB], --remove_db [REMOVE_DB]
                        Removes the entire GAL related databases
  -v {none,debug,info,warning,error,d,e,i,w}, --verbose {none,debug,info,warning,error,d,e,i,w}
                        verbose level: debug, info (default), warning, error
  -log LOG_FILE, --log_file LOG_FILE
                        log file

```

### Upload a Genome data
Usage to upload a genome
```commandline
galEupy -db <db_configuration_file> -org <organism_configuration_file> -path <path_configuration_file> -v d -upload All
```
Both database and organism configuration files are required to upload the genome. Configuration files are in ini format. 

#### Format for database configuration file

```commandline
[dbconnection]
db_username : 
db_password :
host : 
database_prefix: 
port:
```
#### Format for organism configuration file

```commandline
[OrganismDetails]
Organism:
version: 1
source_url:

[SequenceType]
SequenceType: chromosome
scaffold_prefix:

[filePath]
GenBank:
FASTA:
GFF:
Product:
SignalP:
pfam:
TMHMM:
interproscan:
```

### View GAL database log
Usage:
```commandline
galEupy -v d -db <db_configuration_file> -info
```

### Remove an organism from gal database
Usage
```commandline
galEupy -v d -db <db_configuration_file> -org <organism_configuration_file> -remove_org
```
Here, it finds the organism details for the organism configuration file and then deletes the records related it.

### Remove entire GAL related databases
Usage
```commandline
galEupy -v d -db <db_configuration_file> -remove_db
```
The above commands finds the GAL database names from `database_prefix` entry in `<db_configuration_file>` and delete database `database_prefix + _dots` and `database_prefix + _sres`.
Upon running the commands, it asks to confirm the operation. 
