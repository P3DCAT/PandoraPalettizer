from .BamObject import BamObject
from .BamGlobals import *

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
        num_groups = di.get_int32()
        self.group_ids = [read_pointer(di) for i in range(num_groups)] # PaletteGroup

    def write(self, write_version, dg):
        dg.add_int32(len(self.group_ids))

        for group_id in self.group_ids:
            write_pointer(dg, group_id)

    def __str__(self):
        return 'PaletteGroups(group_ids={0})'.format(self.group_ids)