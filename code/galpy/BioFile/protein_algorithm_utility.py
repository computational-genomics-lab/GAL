import re


def parse_hmmscan_result(file, upload_file, id_list):
    fh = open(file, 'r')
    pfam_write_fh = open(upload_file, 'w')
    hmm_row_id = id_list[0]

    for i, line in enumerate(fh):
        line = line.rstrip()
        if not line.startswith("#"):
            line_list = line.split()
            list_len = len(line_list)
            if list_len > 19:
                line_list[18:list_len] = [' '.join(line_list[18:list_len])]
            list_len = len(line_list)
            if list_len == 19:
                hmm_string = process_hmm_scan_single_line(line_list)
                hmm_row_id += 1
                hmm_string1 = '{}\t{}\n'.format(hmm_row_id, hmm_string )
                pfam_write_fh.write(hmm_string1)


def process_hmm_scan_single_line(line_list):
    domain_name = line_list[0]
    accession_id = line_list[1]
    gi_id = line_list[2]
    e_value = line_list[7]
    score = line_list[8]
    bias = line_list[9]
    domain_des = line_list[18]
    match_obj = re.search(r"gi='(.*)'", gi_id, re.M | re.I)
    if match_obj:
        gi_id = match_obj.group(1)
        hmm_string = '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(gi_id, e_value, score, bias, accession_id, domain_name,
                                                         domain_des)
        return hmm_string


def process_signalp_result(file, upload_file, id_list):
    fh = open(file, 'r')
    signalp_write_fh = open(upload_file, 'w')
    signalp_row_id = id_list[2]

    for i, line in enumerate(fh):
        line = line.rstrip()
        if not line.startswith("#"):
            line_list = line.split()
            list_len = len(line_list)
            if list_len == 12:
                gi_id = get_gi_id(line_list[0])
                y_score = line_list[3]
                y_pos = line_list[4]
                d_score = line_list[8]
                status = line_list[9]
                s_string = '{}\t{}\t{}\t{}\t{}'.format(gi_id, y_score, y_pos, d_score, status)
                signalp_row_id += 1
                s_string1 = '{}\t{}\n'.format(signalp_row_id, s_string)
                signalp_write_fh.write(s_string1)


def process_tmhmm_result(file, upload_file, id_list):
    fh = open(file, 'r')
    tmhmm_write_fh = open(upload_file, 'w')
    tmhmm_row_id = id_list[1]
    for i, line in enumerate(fh):
        line = line.rstrip()
        if not line.startswith("#"):
            line_list = line.split()
            list_len = len(line_list)
            if list_len == 5:
                if line_list[2] == 'TMhelix':
                    gi_id = get_gi_id(line_list[0])
                    helix_position = '{}-{}'.format(line_list[3], line_list[4])
                    tmhmm_row_id += 1
                    string1 = '{}\t{}\t\t\t{}\n'.format(tmhmm_row_id, gi_id, helix_position)
                    tmhmm_write_fh.write(string1)


def get_gi_id(string):
    match_obj = re.search(r"gi='(.*)'", string, re.M | re.I)
    if match_obj:
        gi_id = match_obj.group(1)
        return gi_id
