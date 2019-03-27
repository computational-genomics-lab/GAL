import os
import subprocess
import sys
from pathlib import Path, PurePosixPath


def protein_format_db(program, query_sequence_file, target_output, logger):
    # command_option = "formatdb -i {} -p T -n {}".format(query_sequence_file, target_output)
    target_output = Path(target_output)
    log_file = target_output.with_name(target_output.name + ".log")

    # log_file = target_output + ".log"

    command_option = "{} -in {} -dbtype prot -out {} -logfile {}".format(program, query_sequence_file, target_output,
                                                                         log_file)
    process = subprocess.Popen(command_option, shell=True)
    process.wait()
    logger.info("{} run complete for protein data".format(program))


def nucleotide_format_db(program, query_sequence_file, target_output, logger):
    # command_option = "formatdb -i {} -p F -n {}".format(query_sequence_file, target_output)

    # log_file = target_output + ".log"
    target_output = Path(target_output)
    log_file = target_output.with_name(target_output.name + ".log")

    command_option = "{} -in {} -dbtype nucl -out {} -logfile {}".format(program, query_sequence_file, target_output,
                                                                         log_file)
    process = subprocess.Popen(command_option, shell=True)
    process.wait()
    logger.info("{} run complete for nucleotide data".format(program))


def run_augustus(program, species, query_sequence_file, gff_output, logger):
    logger.info("Running augustus gene prediction program...")

    cmd = "{} --outfile={}  --species={} {}".format(program, gff_output, species, query_sequence_file)
    # cmd = "augustus --outfile=" + gff_output + " --species=" + species + " " + query_sequence_file
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    logger.info("Gene Prediction program ran successfully...")


def run_genemark(program, model_file_path, species, query_sequence_file, output, logger):
    logger.info("Running geneMark gene prediction program...")
    # gff_out = output + ".gff"
    # protein_out = output + ".aa"

    output = Path(output)
    gff_out = output.with_name(output.name + ".gff")
    protein_out = output.with_name(output.name + ".aa")

    # program = '/home/arijit/gal_soft/genemark_suite_linux_64/gmsuite/gmhmmp'
    # model_file_path = '/home/arijit/gal_soft/genemark_suite_linux_64/pro_genome/model_file'

    model_file = os.path.join(model_file_path, species)
    cmd = "{} -f 3 -m {} -o {} -A {} {}".format(program, model_file, gff_out, protein_out, query_sequence_file)

    #  logger.info('command line: {}'.format(cmd))
    try:
        process = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        logger.info("Genemark succeeded, result=%s" % (str(process)))
    except subprocess.CalledProcessError as e:
        logger.error("'%s' failed, returned code %s" % (cmd, e.stderr))
        logger.rrror('Error: {}'.format(e.output))

    except OSError as e:
        logger.info("failed to execute program '%s': '%s'" % (cmd, str(e)))
    except Exception as e:
        logger.info('Error occurred')
        logger.error(e.__traceback__)
        logger.error(e)
    finally:
        if not os.path.isfile(gff_out) or not os.path.isfile(protein_out):
            logger.error('Error GeneMark run is not complete')
            sys.exit(0)
        else:
            logger.info('GeneMark Run Complete')


def fetch_protein(gal_path, gff_output):
    """
    This function runs an external program(augustus script) to fetch_protein sequences from the Augustus output

    perl getAnnoFasta.pl gff_output
    """

    script_path = str(gal_path) + "/data/externalProgram/getAnnoFasta.pl"
    cmd = "perl %s %s" % (script_path, gff_output)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()


def run_blast(program, query, output, path, logger):
    """
    This function runs an external program(NCBI Blast) to find annotation information
    """
    logger.info("Running BLASTP against Pfam database")
    # db_path = path + "/data/BlastDB/gal"
    db_path = PurePosixPath(path, 'data/BlastDB/gal')
    # program = 'blastp'
    cmd = "{} -query {} -db {} -num_descriptions 2 -num_alignments 2 -out {} ".format(program, query, db_path, output)
    try:
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        logger.info("BLASTP run complete")
    except Exception as e:
        logger.error('Error occurred: {}'.format(e))


def run_lastz(program, query_file, target_file, output, logger):
    """
    The general format of the LASTZ command line is
    lastz <target> [<query>] [<options>]
    """
    # program = '/home/arijit/lastz-distrib/bin/lastz'

    cmd = """{} '{}'[multiple,unmask] '{}'[unmask] --ambiguous=iupac --ambiguous=n --format=sam --output='{}'
     --chain --gapped""".format(program, target_file, query_file, output)
    # logger.info(cmd)
    try:
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
    except:
        logger.error('Error while running lastz progra: {}'.format(cmd))


def run_signal_p(program_path, query_file, output_file, logger, org_type='euk'):
    logger.info("Running SignalP program....")
    # program_path = "/usr/adadata/GAL/software/signalp-4.1/signalp"
    org_type_option = '-t {}'.format(org_type)

    log_file = output_file.with_name(output_file.name + ".log")

    log_option = '-v -l {}'.format(log_file)
    cmd_string = '{} -f short {} {} {} > {}'.format(program_path, org_type_option, log_option, query_file, output_file)
    process = subprocess.Popen(cmd_string, shell=True)
    process.wait()
    logger.info("SignalP Run complete......")


def run_hmmpfam(program, pfam_db, query_file, output_file, logger):
    logger.info("Running HmmScan program......")
    # program = 'hmmscan'
    # pfam_db = "/usr/adadata/GAL/software/pfam/Pfam-A.hmm"
    output_file_name = output_file.with_name(output_file.name + '_std')

    cmd = '{} -o {} --tblout {} {} {}'.format(program, output_file_name, output_file, pfam_db, query_file)

    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    logger.info("HmmScan Run complete......")


def run_tmhmm(program, query_file, output_file, logger):
    logger.info("Running TmHmm program......")
    # program = "/usr/adadata/GAL/software/tmhmm-2.0c/bin/tmhmm"

    cmd = '{} -workdir=Null {} > {}'.format(program, query_file, output_file)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    logger.info("TMHMM Run complete......")
