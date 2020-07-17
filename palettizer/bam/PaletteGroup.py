from .BamObject import BamObject
from .PaletteGroups import PaletteGroups
from .BamGlobals import *

"""
  REPALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class PaletteGroup(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    @property
    def placements(self):
        return [self.bam_file.get_object(placement_id) for placement_id in self.placement_ids]

    @property
    def pages(self):
        return [self.bam_file.get_object(page_id) for page_id in self.page_ids]

    def load(self, di):
        self.name = di.get_string()
        self.dirname = di.get_string()
        self.palette_groups = self.load_type(PaletteGroups, di)
        self.dependency_level = di.get_int32()
        self.dependency_order = di.get_int32()
        self.dirname_order = di.get_int32()

        num_placements = di.get_uint32()
        self.placement_ids = [read_pointer(di) for i in range(num_placements)] # TexturePlacement

        num_pages = di.get_uint32()
        self.page_ids = [read_pointer(di) for i in range(num_pages)] # PalettePage

        if PI_VERSION >= 19:
            self.has_margin_override = di.get_bool()
            self.margin_override = di.get_int16()
        else:
            self.has_margin_override = False
            self.margin_override = 0

    def write(self, write_version, dg):
        dg.add_string(self.name)
        dg.add_string(self.dirname)
        self.palette_groups.write(write_version, dg)
        dg.add_int32(self.dependency_level)
        dg.add_int32(self.dependency_order)
        dg.add_int32(self.dirname_order)

        dg.add_uint32(len(self.placement_ids))

        for placement_id in self.placement_ids:
            write_pointer(dg, placement_id)

        dg.add_uint32(len(self.page_ids))

        for page_id in self.page_ids:
            write_pointer(dg, page_id)

        if PI_VERSION >= 19:
            dg.add_bool(self.has_margin_override)
            dg.add_int16(self.margin_override)

    def __str__(self):
        return 'PaletteGroup(name={0}, dirname={1}, palette_groups={2}, dependency_level={3}, dependency_order={4}, dirname_order={5}, placement_ids={6}, page_ids={7}, has_margin_override={8}, margin_override={9})'.format(
            self.name,
            self.dirname,
            self.palette_groups,
            self.dependency_level,
            self.dependency_order,
            self.dirname_order,
            self.placement_ids,#', '.join([str(placement) for placement in self.placements]),
            self.page_ids,#', '.join([str(page) for page in self.pages]),
            self.has_margin_override,
            self.margin_override
        )
