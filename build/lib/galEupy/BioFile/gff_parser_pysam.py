import pysam


class GffReader:
    def __init__(self, gff_file):
        self.gff_file = gff_file
        self.gff_obj = open(self.gff_file, "r")

    def get_contents(self):
        # Iterate over the lines in the file
        for line in self.gff_obj:
            # Skip comment lines
            if line.startswith("#"):
                continue
           
            break
