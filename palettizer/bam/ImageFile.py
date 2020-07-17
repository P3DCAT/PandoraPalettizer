from .BamObject import BamObject
from .TextureProperties import TextureProperties
from .BamGlobals import *

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class ImageFile(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    def load(self, di):
        self.properties = self.load_type(TextureProperties, di)
        self.filename = di.get_string()
        self.alpha_filename = di.get_string() # Always empty on source image

        if PI_VERSION >= 10:
            self.alpha_file_channel = di.get_uint8()
        else:
            self.alpha_file_channel = 0

        self.size_known = di.get_bool()
        self.x_size = di.get_int32()
        self.y_size = di.get_int32()

    def write(self, write_version, dg):
        self.properties.write(write_version, dg)
        dg.add_string(self.filename)
        dg.add_string(self.alpha_filename)

        if PI_VERSION >= 10:
            dg.add_uint8(self.alpha_file_channel)

        dg.add_bool(self.size_known)
        dg.add_int32(self.x_size)
        dg.add_int32(self.y_size)

    def __str__(self):
        return 'ImageFile(properties={0}, filename={1}, alpha_filename={2}, alpha_file_channel={3}, size_known={4}, x_size={5}, y_size={6})'.format(
            self.properties,
            self.filename,
            self.alpha_filename,
            self.alpha_file_channel,
            self.size_known,
            self.x_size,
            self.y_size
        )
