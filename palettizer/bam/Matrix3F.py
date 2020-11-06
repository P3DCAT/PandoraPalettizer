from p3bamboo.BamObject import BamObject

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class Matrix3F(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    def load(self, di):
        BamObject.load(self, di)

        self.data = [[self.bam_file.read_stdfloat(di) for j in range(3)] for i in range(3)]

    def write(self, write_version, dg):
        BamObject.write(self, write_version, dg)

        for i in range(3):
            for j in range(3):
                self.bam_file.write_stdfloat(dg, self.data[i][j])

    def __str__(self):
        return 'Matrix3F({0})'.format(self.data)
