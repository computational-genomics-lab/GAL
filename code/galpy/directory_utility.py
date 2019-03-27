import os
import re
import errno
from pathlib import Path, PurePosixPath


def create_protein_feature_directory(upload_path):
    directory_name = "ProteinFeatureData"
    path = create_directory(upload_path, directory_name)
    return path


def create_blast_feature_directory(upload_path):
    nucleotide_directory_name = "output"
    protein_blast_directory_name = "protein_output"
    path1 = create_directory(upload_path, nucleotide_directory_name)
    path2 = create_directory(upload_path, protein_blast_directory_name)
    return path1, path2


def create_directory(upload_path, directory_name):
    """It creates a directory under the upload path"""
    directory = Path(upload_path, directory_name)
    if not directory.exists():
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except (FileExistsError, FileNotFoundError) as e:
            raise e
    '''
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    '''
    return directory


class ProteinFeatureFileName:
    def __init__(self, upload_path, random_string):
        self.feature_path = create_protein_feature_directory(upload_path)

        self.PFam = PurePosixPath(self.feature_path, "HmmPFam.parsed")
        self.TmHmm = PurePosixPath(self.feature_path, "TmHmm.parsed")
        self.SignalP = PurePosixPath(self.feature_path, "SignalP.parsed")

        self.PFam_out = PurePosixPath(self.feature_path, random_string+'.PFam')
        self.TmHmm_out = PurePosixPath(self.feature_path, random_string + '.TmHmm')
        self.SignalP_out = PurePosixPath(self.feature_path, random_string + '.SignalP')


class GalFileName:
    def __init__(self, upload_dir):
        # upload_dir = os.path.abspath(upload_dir)
        upload_dir = Path(upload_dir)
        # if os.path.exists(upload_dir):
        if upload_dir.exists():
            # upload_dir = '/'.join(upload_dir.split('\\'))

            self.NaSequenceImp = PurePosixPath(upload_dir, "NASequenceImp.parsed")
            self.NaFeatureImp = PurePosixPath(upload_dir, "NAFeatureImp.parsed")
            self.NaLocation = PurePosixPath(upload_dir, "NALocation.parsed")
            self.GeneInstance = PurePosixPath(upload_dir, "geneInstance.parsed")
            self.Protein = PurePosixPath(upload_dir, "Protein.parsed")

            # self.NaSequenceImp = '/'.join(self.NaSequenceImp.split('\\'))
            # self.NaFeatureImp = '/'.join(self.NaFeatureImp.split('\\'))
            # self.NaLocation = '/'.join(self.NaLocation.split('\\'))
            # self.GeneInstance = '/'.join(self.GeneInstance.split('\\'))
            # self.Protein = '/'.join(self.Protein.split('\\'))

        else:
            print("Error: Upload Path has some issue....\n")

        # self.NaSequenceImp = upload_dir + "NASequenceImp.parsed"
        # self.NaFeatureImp = upload_dir + "NAFeatureImp.parsed"
        # self.NaLocation = upload_dir + "NALocation.parsed"
        # self.GeneInstance = upload_dir + "geneInstance.parsed"
        # self.Protein = upload_dir + "Protein.parsed"


class GALFileHandler(GalFileName):
    def __init__(self, upload_dir):
        GalFileName.__init__(self, upload_dir)

        self.NaSequenceImp_fh = open(self.NaSequenceImp, "w")
        self.NaFeatureImp_fh = open(self.NaFeatureImp, 'w')
        self.NALocation_fh = open(self.NaLocation, 'w')
        self.GeneInstance_fh = open(self.GeneInstance, 'w')
        self.Protein_fh = open(self.Protein, 'w')
