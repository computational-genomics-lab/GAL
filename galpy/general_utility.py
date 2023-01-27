import re
import random
import datetime
import logging
_logger = logging.getLogger("galpy.general_utility")


def reverse_complement(sequence):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    reverse_complement_sequence = "".join(complement.get(base, base) for base in reversed(sequence))
    return reverse_complement_sequence


def translate(dna_string):
    # Translate a given DNA sequence into protein
    protein = []
    table = {
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
        'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
        'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
        'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
        'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
        'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
        'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
        'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
        'TAC': 'Y', 'TAT': 'Y', 'TAA': '_', 'TAG': '_',
        'TGC': 'C', 'TGT': 'C', 'TGA': '_', 'TGG': 'W',
    }
    end = len(dna_string) - (len(dna_string) % 3) - 1
    for i in range(0, end, 3):
        codon = dna_string[i:i + 3]
        codon = codon.upper()
        if codon in table:
            amino_acid = table[codon]
            protein.append(amino_acid)
        else:
            protein.append("N")

    return "".join(protein)


def read_fasta_to_dictionary(genome_file):
    """
    this function reads a sequence file in FASTA format and stores
    in a dictionary format for future manipulation
    """
    filename = genome_file
    dct = {}

    id_name = ""
    sequence = ""
    first_pass = 1

    read_fh = open(filename, 'r')
    for i, line in enumerate(read_fh):
        line = line.rstrip()
        if re.search(r'^>(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(.*)', line):

            match_obj = re.search(r'^>(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(\s+)(\S+)(.*)', line)
            if not first_pass:
                dct[id_name] = sequence
            id_name = match_obj.group(1)
            id_name = re.sub(r',', "", id_name)
            first_pass = 0
            sequence = ""

        elif re.search(r'^>(\S+)(.*)', line):

            match_obj = re.search(r'^>(\S+)(.*)', line)
            if not first_pass:
                dct[id_name] = sequence
            id_name = match_obj.group(1)
            id_name = re.sub(r'(\d+)_', "", id_name)
            id_name = re.sub(r'.*\|', "", id_name)
            first_pass = 0
            sequence = ""
        else:
            sequence += line
    dct[id_name] = sequence

    return dct


def product_to_dictionary(filename):
    dct = {}
    read_fh = open(filename, 'r')
    for i, line in enumerate(read_fh):
        line = line.rstrip()
        if re.search(r'^#', line):
            continue
        tmp = re.split(r'\t', line)
        if len(tmp) == 2:
            dct[tmp[0]] = tmp[1]
    return dct


def random_string(length=10):
    valid_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return ''.join((random.choice(valid_letters) for i in range(length)))


def get_date():
    i = datetime.datetime.now()
    today = '{}-{}-{}'.format(i.year, i.month, i.day)
    return today


class BaseCount:
    def __init__(self, sequence):
        self.sequence = sequence
        self.A_count = len(re.findall("(?i)a", self.sequence))
        self.T_count = len(re.findall("(?i)t", self.sequence))
        self.G_count = len(re.findall("(?i)g", self.sequence))
        self.C_count = len(re.findall("(?i)c", self.sequence))

    def length(self):
        return len(self.sequence)

    def other_count(self):
        count = len(self.sequence) - self.A_count - self.T_count - self.G_count - self.C_count
        return count

    def print_base_count(self):
        other_count = self.other_count()
        return '{}\t{}\t{}\t{}\t{}'.format(self.A_count, self.T_count, self.G_count, self.C_count, other_count)