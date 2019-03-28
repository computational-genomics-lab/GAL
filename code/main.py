from galpy import data_schedule_utility
from galpy.BioFile import sam_parser
from galpy import gal_function, config_utility, db_function, schema_function, db_table_utility
from galpy import shared_resource_data as sres_data, organism_function as org_function
from galpy import basic_utility, logging_utility, command_argument
from galpy import db_table_utility as db_table
from galpy import blast_set
from pathlib import Path, PurePath, PurePosixPath


def main(arg, db_config, logger, content_dir):
    while 1:
        status = data_schedule_utility.StatusLog(db_config)
        log_dict = status.get_upload_log()
        if 'Running' in log_dict:
            logger.warning('One program is already running')
            break
        elif 'Submitted' in log_dict:
            logger.info('One input is ready to run')

            submission_list = status.get_submit_list()

            for i, value in enumerate(submission_list):
                config_path = Path(value['ORGANISM_CONFIG_PATH'])
                upload_process_id = value['UPLOAD_PROCESS_ID']

                update_status_log = data_schedule_utility.UpdateStatusLog(db_config, upload_process_id)
                update_status_log.status_running()
                update_status_log.stage_central_dogma()

                config = gal_function.ConfigFileHandler(arg.db_config_file, arg.path_config_file, config_path, logger)
                db_config = config.db_config
                org_config = config.org_config
                path_config = config.path_config

                org_exist = org_function.check_organism_existence(db_config, org_config.organism, org_config.version,
                                                                  arg.log_file)

                if org_exist:
                    update_status_log.status_organism_exist()
                    update_status_log.stage_skipped()

                elif org_exist is False:
                    try:
                        random_string = basic_utility.random_string(20)
                        id_list = db_table_utility.get_table_status(db_config, arg.log_file)
                        gal_function.process_central_dogma_data(config, random_string, id_list, content_dir, arg.log_file)

                        taxonomy_dct = org_function.update_organism_table(db_config, org_config.organism,
                                                                          org_config.version, arg.log_file)
                        taxonomy_id = taxonomy_dct['TAXON_ID']
                        logger.debug('Functional annotation: start')
                        update_status_log.stage_functional_annotation()

                        blast_set.create_row_files(db_config, taxonomy_id, org_config.organism, org_config.version,
                                                   path_config, arg.log_file)
                        
                        # protein Feature algorithms
                        gal_function.process_protein_feature_algorithm_data(config, random_string, taxonomy_dct, arg.log_file)

                        gal_function.process_interpro_data(db_config, org_config, path_config, taxonomy_id, arg.log_file)
                        logger.debug('Functional annotation: ended')
                        organism_count = org_function.organism_count(db_config)

                        if organism_count > 1:
                            update_status_log.stage_comparative_genomcis()
                            logger.debug('Comparative Genomics: started')
                            sam_id = db_table.get_sam_alignment_last_row_id(db_config)
                            sam_parser.process_sam_alignment(db_config, path_config, sam_id, arg.log_file)
                            logger.debug('Comparative Genomics: ended')
                        update_status_log.status_complete()
                        update_status_log.status_complete()
                    except Exception as e:
                        logger.error('Exception occurred: {}'.format(e))
                        update_status_log.status_failed()

                    return 0

        else:
            break


def process_schema_common_data(db_config, arg, content_dir):

    db_function.check_db_connection(db_config.host, db_config.db_username, db_config.db_password)
    schema_function.database_schema(db_config, content_dir, arg.log_file)

    sres_data.common_data_basic(db_config, content_dir, arg.log_file)

