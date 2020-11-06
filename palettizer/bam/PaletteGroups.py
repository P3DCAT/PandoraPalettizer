from p3bamboo.BamObject import BamObject

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class PaletteGroups(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    @property
    def groups(self):
        return [self.bam_file.get_object(group_id) for group_id in self.group_ids]

    def load(self, di):
        BamObject.load(self, di)

        self.group_ids = self.bam_file.read_pointer_int32_list(di) # PaletteGroup

    def write(self, write_version, dg):
        BamObject.write(self, write_version, dg)

        self.bam_file.write_pointer_int32_list(dg, self.group_ids)

    def __str__(self):
        return 'PaletteGroups(group_ids={0})'.format(self.group_ids)
