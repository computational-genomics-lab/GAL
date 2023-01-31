from pathlib import Path, PurePosixPath
import logging
_logger = logging.getLogger("galpy.directory_utility")


class BaseUploadDirectory:
    def __init__(self, upload_dir):
        """ class constructor creates a directory if the upload directory doesn;t exist
        parameters
        ---------
        upload_dir: basestring

        """
        self.upload_dir = Path(upload_dir)
        if not self.upload_dir.exists():
            self.upload_dir = Path("GALUploadTmp")
            if not self.upload_dir.exists():
                self.create_directory(self.upload_dir)

        _logger.info("Upload path: {}".format(self.upload_dir))

    @staticmethod
    def create_directory(directory):
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except (FileExistsError, FileNotFoundError) as e:
            raise e


class UploadDirectory(BaseUploadDirectory):
    def __init__(self, upload_dir):
        BaseUploadDirectory.__init__(self, upload_dir)

        self.NaSequenceImp = self.upload_dir.joinpath("NASequenceImp.parsed")
        self.NaFeatureImp = self.upload_dir.joinpath("NAFeatureImp.parsed")
        self.NaLocation = self.upload_dir.joinpath("NALocation.parsed")
        self.GeneInstance = self.upload_dir.joinpath("geneInstance.parsed")
        self.Protein = self.upload_dir.joinpath("Protein.parsed")

    def protein_feature_directory(self):
        directory_name = "ProteinFeatureData"
        directory_path = self.upload_dir.joinpath(directory_name)
        self.create_directory(directory_path)
        return directory_path

    def blast_feature_directory(self):
        nucleotide_directory_name = "output"
        protein_blast_directory_name = "protein_output"
        nucleotide_directory_path = self.upload_dir.joinpath(nucleotide_directory_name)
        protein_blast_directory_path = self.upload_dir.joinpath(protein_blast_directory_name)
        self.create_directory(nucleotide_directory_path)
        self.create_directory(protein_blast_directory_path)
        return nucleotide_directory_path, protein_blast_directory_path


class GALFileHandler(UploadDirectory):
    def __init__(self, upload_dir):
        UploadDirectory.__init__(self, upload_dir)
        _logger.info('Reset the temporary files')
        self.NaSequenceImp_fh = open(self.NaSequenceImp, "w")
        self.NaFeatureImp_fh = open(self.NaFeatureImp, 'w')
        self.NALocation_fh = open(self.NaLocation, 'w')
        self.GeneInstance_fh = open(self.GeneInstance, 'w')
        self.Protein_fh = open(self.Protein, 'w')


class ProteinAnnotationFiles(UploadDirectory):
    def __init__(self, upload_path, random_string,  default_dir_name='ProteinFeatureData'):
        UploadDirectory.__init__(self, upload_path)

        self.feature_path = Path(upload_path).joinpath(default_dir_name)
        self.create_directory(self.feature_path)

        self.PFam = self.feature_path.joinpath("HmmPFam.parsed")
        self.TmHmm = self.feature_path.joinpath("TmHmm.parsed")
        self.SignalP = self.feature_path.joinpath("SignalP.parsed")

        self.PFam_out = self.feature_path.joinpath(f"{random_string}.PFam")
        self.TmHmm_out = self.feature_path.joinpath(f"{random_string}.TmHmm")
        self.SignalP_out = self.feature_path.joinpath(f"{random_string}.SignalP")

