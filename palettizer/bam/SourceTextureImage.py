from .BamObject import BamObject
from .ImageFile import ImageFile
from .BamGlobals import *

"""
  REPALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class SourceTextureImage(ImageFile):

    def __init__(self, bam_file, bam_version):
        ImageFile.__init__(self, bam_file, bam_version)

    @property
    def texture(self):
        return self.bam_file.get_object(self.texture_id)

    def load(self, di):
        ImageFile.load(self, di)
        self.texture_id = read_pointer(di) # TextureImage

    def write(self, write_version, dg):
        ImageFile.write(self, di)
        write_pointer(dg, self.texture_id)

    def __str__(self):
        return 'SourceTextureImage(parent={0}, texture_id={1}'.format(
            super(SourceTextureImage, self).__str__(),
            self.texture_id
        )