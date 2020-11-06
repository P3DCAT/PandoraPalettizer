from p3bamboo.BamObject import BamObject
from palettizer.bam.PaletteGroups import PaletteGroups

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class EggFile(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    @property
    def texture_refs(self):
        return [self.bam_file.get_object(texture_ref_id) for texture_ref_id in self.texture_ref_ids]

    @property
    def default_group(self):
        return self.bam_file.get_object(self.default_group_id)

    def load(self, di):
        BamObject.load(self, di)

        self.name = di.get_string()
        self.current_directory = di.get_string()
        self.source_filename = di.get_string()
        self.dest_filename = di.get_string()
        self.egg_comment = di.get_string()

        self.texture_ref_ids = self.bam_file.read_pointer_uint32_list(di) # TextureReference

        self.explicitly_assigned_groups = self.load_type(PaletteGroups, di)
        self.default_group_id = self.bam_file.read_pointer(di) # PaletteGroup

        self.is_surprise = di.get_bool()
        self.is_stale = di.get_bool()

    def write(self, write_version, dg):
        dg.add_string(self.name)
        dg.add_string(self.current_directory)
        dg.add_string(self.source_filename)
        dg.add_string(self.dest_filename)
        dg.add_string(self.egg_comment)

        dg.add_uint32(len(self.texture_ref_ids))

        for texture_ref_id in self.texture_ref_ids:
            self.bam_file.write_pointer(dg, texture_ref_id)

        self.explicitly_assigned_groups.write(write_version, dg)
        self.bam_file.write_pointer(dg, self.default_group_id)

        dg.add_bool(self.is_surprise)
        dg.add_bool(self.is_stale)

    def __str__(self):
        return 'EggFile(name={0}, current_directory={1}, source_filename={2}, dest_filename={3}, egg_comment={4}, texture_ref_ids={5}, explicitly_assigned_groups={6}, default_group_id={7}, is_surprise={8}, is_stale={9})'.format(
            self.name,
            self.current_directory,
            self.source_filename,
            self.dest_filename,
            self.egg_comment,
            self.texture_ref_ids,
            self.explicitly_assigned_groups,
            self.default_group_id,
            self.is_surprise,
            self.is_stale
        )
