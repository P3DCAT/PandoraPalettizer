from p3bamboo.BamObject import BamObject
from palettizer.bam.ImageFile import ImageFile

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class DestTextureImage(ImageFile):

    def __init__(self, bam_file, bam_version):
        ImageFile.__init__(self, bam_file, bam_version)

    def load(self, di):
        ImageFile.load(self, di)

    def write(self, write_version, dg):
        ImageFile.write(self, write_version, dg)

    def __str__(self):
        return 'DestTextureImage(parent={0})'.format(
            super(DestTextureImage, self).__str__()
        )
