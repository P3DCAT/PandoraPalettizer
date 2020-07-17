from .BamObject import BamObject
from .TextureProperties import TextureProperties
from .BamGlobals import *

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class PalettePage(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    @property
    def group(self):
        return self.bam_file.get_object(self.group_id)

    @property
    def images(self):
        return [self.bam_file.get_object(image_id) for image_id in self.image_ids]

    def load(self, di):
        self.name = di.get_string()
        self.group_id = read_pointer(di) # PaletteGroup
        self.texture_properties = self.load_type(TextureProperties, di)

        num_images = di.get_uint32()
        self.image_ids = [read_pointer(di) for i in range(num_images)] # PaletteImage

    def write(self, write_version, dg):
        dg.add_string(self.name)
        write_pointer(dg, self.group_id)
        self.texture_properties.write(write_version, dg)

        dg.add_uint32(len(self.image_ids))

        for image_id in self.image_ids:
            write_pointer(dg, image_id)

    def __str__(self):
        return 'PalettePage(name={0}, group_id={1}, texture_properties={2}, image_ids={3})'.format(
            self.name,
            self.group_id,
            self.texture_properties,
            self.image_ids)