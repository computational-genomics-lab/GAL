from galeupy import organism_function


class StatusLog:
    def __init__(self, db_config):
        self.db_dots = organism_function.create_db_connection(db_config)

    def submit_log(self, organism_name, organism_version, path_config_file):

        upload_status_id = 1  # upload_status_id: name: submitted
        upload_stage_id = 1  # upload_stage_id: name: Waiting to Start

        query = """INSERT INTO DataProcessLog(ORGANISM_NAME, ORGANISM_VERSION, ORGANISM_CONFIG_PATH, UPLOAD_STATUS_ID, 
            UPLOAD_STAGE_ID) VALUES ('{}', {}, '{}', '{}', '{}')""".format(organism_name, organism_version,
                                                                           path_config_file, upload_status_id,
                                                                           upload_stage_id)
        self.db_dots.insert(query)

    def get_submit_list(self):
        query = "SELECT *  FROM DataProcessLog WHERE UPLOAD_STATUS_ID = 1 ORDER BY INITIAL_SUBMISSION_TIME"
        result = self.db_dots.query(query)
        return result

    def get_upload_log(self):

        query = """SELECT US.STATUS, US.UPLOAD_STATUS_ID, COUNT(DPL.UPLOAD_PROCESS_ID) AS 'count' 
        FROM DataProcessLog DPL, UploadStatus US
        WHERE  DPL.UPLOAD_STATUS_ID = US.UPLOAD_STATUS_ID
        GROUP BY UPLOAD_STATUS_ID"""

        result = self.db_dots.query(query)

        data_dict = {}
        for i, value in enumerate(result):
            status = value['STATUS']
            count = value['count']
            data_dict[status] = count

        return data_dict


class UpdateStatusLog:
    def __init__(self, db_config, log_id):
        self.db_dots = organism_function.create_db_connection(db_config)
        self.log_id = log_id

    def status_update_query_general(self, status_id):
        """
            1 = 'Submitted'
            2 = 'Running'
            3 = 'Failed'
            4 = 'Complete'
            5 = 'Organism already exist'

            :param status_id:
            :return:
        """
        query = """UPDATE DataProcessLog  SET UPLOAD_STATUS_ID = {}
            WHERE upload_process_id = {}""".format(status_id, self.log_id)
        return query

    def status_update_query_start(self, status_id):
        """
            1 = 'Submitted'
            2 = 'Running'
            3 = 'Failed'
            4 = 'Complete'
            5 = 'Organism already exist'

            :param status_id:
            :return:
        """
        query = """UPDATE DataProcessLog  SET UPLOAD_STATUS_ID = {}, START_TIME = now()
            WHERE upload_process_id = {}""".format(status_id, self.log_id)
        return query

    def status_update_query_end(self, status_id):
        """
            1 = 'Submitted'
            2 = 'Running'
            3 = 'Failed'
            4 = 'Complete'
            5 = 'Organism already exist'

            :param status_id:
            :return:
        """
        query = """UPDATE DataProcessLog  SET UPLOAD_STATUS_ID = {}, END_TIME = now()
            WHERE upload_process_id = {}""".format(status_id, self.log_id)
        return query

    def stage_update_query(self, stage_id):
        """
            1 = 'Waiting to Start'
            2 = 'Central Dogma'
            3 = 'Gene Prediction'
            4 = 'Blast Program running'
            5 = 'Functional Annotation'
            6 = 'Comparative Genomics'
            7 = 'Upload Complete'
            8 = 'Skipped'
            9 = 'Unknown'

            :param stage_id:
            :return:
        """

        query = """UPDATE DataProcessLog  SET UPLOAD_STAGE_ID = {}, MODIFICATION_TIME = now()
                           WHERE upload_process_id = {}""".format(stage_id, self.log_id)

        return query

    def status_submit(self):
        # 1 = 'Submitted'
        status_id = 1
        query = self.status_update_query_general(status_id)
        self.db_dots.insert(query)

    def status_running(self):
        # 2 = 'Running'
        status_id = 2
        query = self.status_update_query_start(status_id)
        self.db_dots.insert(query)

    def status_failed(self):
        # 3 = 'Failed'
        status_id = 3
        query = self.status_update_query_end(status_id)
        self.db_dots.insert(query)

    def status_complete(self):
        # 4 = 'Complete'
        status_id = 4
        query = self.status_update_query_end(status_id)
        self.db_dots.insert(query)

    def status_organism_exist(self):
        # 5 = 'Organism already exist'
        status_id = 5
        query = self.status_update_query_end(status_id)
        self.db_dots.insert(query)

    def stage_waiting(self):
        # 1 = 'Waiting to Start'
        stage_id = 1
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)

    def stage_central_dogma(self):
        # 2 = 'Central Dogma'
        stage_id = 2
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)

    def stage_gene_prediction(self):
        # 3 = 'Gene Prediction'
        stage_id = 3
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)

    def stage_blast_annotation(self):
        # 4 = 'Blast Program running'
        stage_id = 4
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)

    def stage_functional_annotation(self):
        # 5 = 'Functional Annotation'
        stage_id = 5
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)

    def stage_comparative_genomcis(self):
        # 6 = 'Comparative Genomics'
        stage_id = 6
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)

    def stage_upload_complete(self):
        # 7 = 'Upload Complete'
        stage_id = 7
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)

    def stage_skipped(self):
        # 8 = 'Skipped'
        stage_id = 8
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)

    def stage_unknown(self):
        # 9 = 'Unknown'
        stage_id = 9
        query = self.stage_update_query(stage_id)
        self.db_dots.insert(query)



