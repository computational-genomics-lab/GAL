import re
from pyparsing import *


def parse_file(filename, **kw):
    fp = open(filename)
    ignore_no_hits = False
    dct = {}
    for record in BlastFile(fp, ignore_no_hits):
        errfp = None
        a = record.find("Query=")
        if a > 0:
            record = record[a:]
        blast_record = BlastParser()
        parse_results = blast_record._construct_parser(record)
        fetch_data_from_blast_parser(parse_results)
        new_dct = fetch_data_from_blast_parser(parse_results)
        dct.update(new_dct)
    return dct


def fetch_data_from_blast_parser(parse_result):
    query_name = parse_result.query_name[0]

    # m = re.compile('.t\d$')
    # query_name = m.sub('', query_name)

    dct = {}
    if 'hits' in parse_result.keys():
        query_annotation = 'Hypothetical Protein'
    else:
        query_annotation = parse_result.All_header[0]
        query_annotation = re.sub(r"\n", " ", query_annotation)

    dct[query_name] = query_annotation
    return dct


class BlastFile:
    CHUNKSIZE = 10 * 1024 * 1024
    blast_marker = re.compile('^(BLASTX|BLASTN|BLASTP|TBLASTX|TBLASTN)', re.MULTILINE)
    query_marker = '\nQuery='
    no_hits_marker = "***** No hits found ******"

    def __init__(self, fp, ignore_no_hits=False):
        self.first = True
        self.fp = fp
        self.ignore_no_hits = ignore_no_hits
        self.total = 0

        self.s = ""
        self.pos = 0
        self.stopped = False
        self._more()

        if not self.blast_marker.match(self.s):
            raise Exception("this doesn't look like a BLAST file")

    def _more(self):
        r = self.fp.read(self.CHUNKSIZE)
        if not r:
            raise StopIteration
        self.s = self.s[self.pos:] + r
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.stopped:
            raise StopIteration

        while 1:
            a = self.s.find(self.query_marker, self.pos)
            if a >= 0:
                b = self.s.find(self.query_marker, a + 1)

            # do we have a complete record?
            if a >= 0 and b > 0:
                record = self.s[self.pos:b]
                self.pos = b
                self.total += 1
                if self.ignore_no_hits and record.find(self.no_hits_marker) >= 0:
                    if self.first:
                        self.first = False
                        return record  # get database info
                else:
                    return record
            else:
                try:
                    self._more()
                except StopIteration:
                    self.stopped = True
                    record, self.s = self.s[self.pos:], ""
                    self.pos = 0
                    return record


def make_comma_int(s):
    return int(s[0].replace(",", ""))


def named_comma_int(name):
    return Word(nums + ',').setParseAction(make_comma_int).copy().setResultsName(name)


def named_int(name):
    return Word(nums).setParseAction(make_int).copy().setResultsName(name)


def make_int(x):
    return int(x[0])


def make_float(x):
    x = x[0]
    if x.startswith('e'):
        x = '1' + x
    return float(x)


def named_float(name):
    return Word(alphanums).setParseAction(make_float).copy().setResultsName(name)


class BlastParser:
    query_marker = 'Query='

    def __init__(self):
        self.reset()

    def reset(self):
        self.blast_database = None

    def _construct_parser(self, record):
        query_size = LineEnd().suppress() + Literal("Length=").suppress() + named_comma_int('query_size')
        query_name = SkipTo(query_size).setResultsName('query_name')
        query_line = Literal("Query=").suppress() + query_name + query_size

        # ***** No hits found ****** part
        no_hits = Literal("***** No hits found *****")
        self.no_hits = SkipTo(no_hits, include=True).setResultsName('hits')

        # Alignment Header
        sequence_name = SkipTo(LineEnd().suppress() + Literal("Length=").suppress(), include=True)
        sequence_name = sequence_name.setResultsName("sequence_name")
        alignment_header_symbol = SkipTo(LineEnd() + Literal(">"), include=True).suppress()
        alignment_header = alignment_header_symbol + sequence_name + named_int('length')

        all_alignment = Group(ZeroOrMore(alignment_header)).setResultsName('All_header')
        self.blast_record = query_line + Optional(self.no_hits) + all_alignment

        self.parse_results = self.blast_record.parseString(record)

        return self.parse_results
