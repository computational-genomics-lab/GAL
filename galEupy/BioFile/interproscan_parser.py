import re
import logging
_logger = logging.getLogger("galEupy.BioFile.interproscan_parser")


class ParseInterproResult:
    def __init__(self, interpro_file, parsed_output_file, gene_name_dct):
        self.interpro_file = interpro_file
        self.parsed_output_file = parsed_output_file
        self.gene_name_dct = gene_name_dct

    def create_parsed_output(self, pif_id=0):
        """This function parse a InterPro formatted file and return database format file """
        ipr_feature = "InterPro"
        go_feature = "GO"
        domain_name = ''

        parsed_fh = open(self.parsed_output_file, 'w')
        pif_id += 1
        read_fh = open(self.interpro_file, 'r')
        for i, line in enumerate(read_fh):
            if re.search(r'^@', line):
                continue
            if re.search(r'^#', line):
                continue
            tmp = re.split(r'\t', line)

            gene_name = tmp[0]

            if gene_name in self.gene_name_dct:
                protein_instance_id = self.gene_name_dct[gene_name]
            else:
                _logger.error(f'{gene_name} name is not matching with the database entry')
                continue
            ip_line_obj = InterProScanLines(tmp, protein_instance_id, pif_id)

            ip_line_obj.db_entry(parsed_fh)
            pif_id = ip_line_obj.pif_id
            """
            start = int(tmp[6])
            stop = int(tmp[7])
            length = stop - start
            pval_mant = tmp[8]
            pval_exp = 0
            common_string = '{}\t{}\t{}\t1\t{}\t{}'.format(start, stop, length, pval_mant, pval_exp)

            if tmp[3] == 'ProSiteProfiles':
                feature_name = "ProfileScan"
            elif tmp[3] == 'SMART':
                feature_name = "HmmSmart"
            elif tmp[3] == 'PRINTS':
                feature_name = "FprintScan"
            else:
                continue

            if len(tmp) > 11:
                if len(tmp) >= 13:
                    domain_name = tmp[12]
                if not re.match(r'^GO', tmp[13]) and re.match(r'^IPR', tmp[11]):
                    ipr = re.split(r'\|', tmp[11])
                    for ipr_value in ipr:
                        print_parsed_result(parsed_fh, pif_id, protein_instance_id, ipr_feature, common_string,
                                            domain_name, ipr_value, '')
                        pif_id += 1

                elif re.match(r'^IPR', tmp[11]) and re.match(r'^GO', tmp[13]):
                    go = re.split(r'\|', tmp[13].rstrip('\n'))
                    prediction_id = tmp[11]
                    for go_value in go:
                        print_parsed_result(parsed_fh, pif_id, protein_instance_id, go_feature, common_string,
                                            domain_name, prediction_id, go_value)
                        pif_id += 1

            prediction_id = tmp[4]
            print_parsed_result(parsed_fh, pif_id, protein_instance_id, feature_name, common_string, domain_name,
                                prediction_id, '')

            pif_id += 1
            """


class InterProScanLines:
    def __init__(self, line_arr, protein_instance_id, pif_id):
        self.line_arr = line_arr
        self.column_count = len(self.line_arr)

        self.protein_instance_id = protein_instance_id
        self.pif_id = pif_id

    def common_string(self):
        if self.column_count == 13:
            start = int(self.line_arr[6])
            stop = int(self.line_arr[7])
            length = stop - start
            pval_mant = self.line_arr[8]
            pval_exp = 0
        elif self.column_count == 15:
            start = int(self.line_arr[8])
            stop = int(self.line_arr[9])
            length = stop - start
            pval_mant = self.line_arr[10]
            pval_exp = 0
        else:
            return 0
        common_string = '{}\t{}\t{}\t1\t{}\t{}'.format(start, stop, length, pval_mant, pval_exp)
        return common_string

    def get_feature_name(self):
        if self.line_arr[3] == 'ProSiteProfiles':
            feature_name = "ProfileScan"
        elif self.line_arr[3] == 'SMART':
            feature_name = "HmmSmart"
        elif self.line_arr[3] == 'PRINTS':
            feature_name = "FprintScan"
        else:
            feature_name = None
        return feature_name

    def domain_name(self):
        domain_name = None
        domain_name = self.line_arr[12]
        return domain_name

    def db_entry(self, parsed_fh):
        ipr_feature = "InterPro"
        go_feature = "GO"
        common_string = self.common_string()
        domain_name = self.domain_name()
        feature_name = self.get_feature_name()

        if not re.match(r'^GO', self.line_arr[11]) and re.match(r'^IPR', self.line_arr[11]):
            ipr = re.split(r'\|', self.line_arr[11])
            for ipr_value in ipr:
                print_parsed_result(parsed_fh, self.pif_id, self.protein_instance_id, ipr_feature, common_string,
                                    domain_name, ipr_value, '')
                self.pif_id += 1

        elif re.match(r'^IPR', self.line_arr[11]) and re.match(r'^GO', self.line_arr[11]):
            go = re.split(r'\|', self.line_arr[11].rstrip('\n'))
            prediction_id = self.line_arr[11]
            for go_value in go:
                print_parsed_result(parsed_fh, self.pif_id, self.protein_instance_id, go_feature, common_string,
                                    domain_name, prediction_id, go_value)
                self.pif_id += 1

        prediction_id = self.line_arr[4]
        print_parsed_result(parsed_fh, self.pif_id, self.protein_instance_id, feature_name, common_string, domain_name,
                            prediction_id, '')

        self.pif_id += 1


def print_parsed_result(parsed_fh, pif_id, protein_instance_id, feature_name, common_string, domain_name, prediction_id, go_id):
    bit_score = 1
    is_reviewed = 0
    string1 = '{}\t{}\t{}\t{}\t{}'.format(pif_id, protein_instance_id, feature_name, feature_name, common_string)
    string2 = '{}\t{}\t{}\t{}\t{}\t{}'.format(bit_score, domain_name, prediction_id, go_id, is_reviewed, 1)
    final_string = '{}\t{}\tNULL\n'.format(string1, string2)
    parsed_fh.write(final_string)
    return final_string




