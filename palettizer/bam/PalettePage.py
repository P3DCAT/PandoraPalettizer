from p3bamboo.BamObject import BamObject
from palettizer.bam.TextureProperties import TextureProperties

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
        BamObject.load(self, di)

        self.name = di.get_string()
        self.group_id = self.bam_file.read_pointer(di) # PaletteGroup
        self.texture_properties = self.load_type(TextureProperties, di)

        self.image_ids = self.bam_file.read_pointer_uint32_list(di) # PaletteImage

    def write(self, write_version, dg):
        BamObject.write(self, write_version, dg)

        dg.add_string(self.name)
        self.bam_file.write_pointer(dg, self.group_id)
        self.texture_properties.write(write_version, dg)

        self.bam_file.write_pointer_uint32_list(dg, self.image_ids)

    def __str__(self):
        return 'PalettePage(name={0}, group_id={1}, texture_properties={2}, image_ids={3})'.format(
            self.name,
            self.group_id,
            self.texture_properties,
            self.image_ids)
