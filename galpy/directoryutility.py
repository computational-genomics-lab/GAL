from pathlib import Path
import logging
_logger = logging.getLogger("galpy.directoryutility")


class UploadDirectory:
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
        self.NaSequenceImp = self.upload_dir.joinpath("NASequenceImp.parsed")
        self.NaFeatureImp = self.upload_dir.joinpath("NAFeatureImp.parsed")
        self.NaLocation = self.upload_dir.joinpath("NALocation.parsed")
        self.GeneInstance = self.upload_dir.joinpath("geneInstance.parsed")
        self.Protein = self.upload_dir.joinpath("Protein.parsed")

    @staticmethod
    def create_directory(directory):
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except (FileExistsError, FileNotFoundError) as e:
            raise e

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

        self.NaSequenceImp_fh = open(self.NaSequenceImp, "w")
        self.NaFeatureImp_fh = open(self.NaFeatureImp, 'w')
        self.NALocation_fh = open(self.NaLocation, 'w')
        self.GeneInstance_fh = open(self.GeneInstance, 'w')
        self.Protein_fh = open(self.Protein, 'w')