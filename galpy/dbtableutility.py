import logging
_logger = logging.getLogger("galpy.dbtableutility")


def get_table_status(db_dots):
    sql_1 = "SELECT MAX(NA_SEQUENCE_ID) as LAST_ID FROM NASequenceImp"
    sql_2 = "SELECT MAX(NA_FEATURE_ID) as LAST_ID FROM NAFeatureImp"
    sql_3 = "SELECT MAX(NA_LOCATION_ID) as LAST_ID FROM NALocation"
    sql_4 = "SELECT MAX(GENE_INSTANCE_ID) as LAST_ID FROM GeneInstance"
    sql_5 = "SELECT MAX(PROTEIN_ID) as LAST_ID FROM Protein"

    row_na_sequence = get_max_table_value(db_dots, sql_1)
    row_na_feature = get_max_table_value(db_dots, sql_2)
    row_na_location = get_max_table_value(db_dots, sql_3)
    row_gene_instance = get_max_table_value(db_dots, sql_4)
    row_protein = get_max_table_value(db_dots, sql_5)

    print_str = """Getting Max IDs of each table..
        NASequenceImp ID: {}
        NAFeatureImp ID: {}
        NALocation ID: {}
        GeneInstance ID: {}
        Protein ID: {}
        """.format(row_na_sequence, row_na_feature, row_na_location, row_gene_instance, row_protein)

    _logger.info(print_str)

    row_list = [row_na_sequence, row_na_feature, row_na_feature, row_na_feature, row_na_feature]
    return row_list


def get_max_table_value(db, query):
    data = db.query_one(query)
    count = data['LAST_ID']
    if count is None:
        max_id = 0
    else:
        max_id = count
    return max_id

