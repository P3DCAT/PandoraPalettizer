from .BamObject import BamObject
from .TexturePosition import TexturePosition
from .BamGlobals import *

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class TexturePlacement(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    @property
    def texture(self):
        return self.bam_file.get_object(self.texture_id)

    @property
    def group(self):
        return self.bam_file.get_object(self.group_id)

    @property
    def image(self):
        return self.bam_file.get_object(self.image_id)

    @property
    def dest_image(self):
        return self.bam_file.get_object(self.dest_image_id)

    def load(self, di):
        self.texture_id = read_pointer(di) # TextureImage
        self.group_id = read_pointer(di) # PaletteGroup
        self.image_id = read_pointer(di) # PaletteImage
        self.dest_image_id = read_pointer(di) # DestTextureImage

        self.has_uvs = di.get_bool()
        self.size_known = di.get_bool()
        self.position = self.load_type(TexturePosition, di)

        self.is_filled = di.get_bool()
        self.placed = self.load_type(TexturePosition, di)
        self.omit_reason = di.get_int32()

        num_references = di.get_int32()
        self.reference_ids = [read_pointer(di) for i in range(num_references)]

        num_texture_swaps = di.get_int32()
        self.texture_swap_ids = [read_pointer(di) for i in range(num_texture_swaps)]

    def write(self, write_version, dg):
        write_pointer(dg, self.texture_id)
        write_pointer(dg, self.group_id)
        write_pointer(dg, self.image_id)
        write_pointer(dg, self.dest_image_id)

        dg.add_bool(self.has_uvs)
        dg.add_bool(self.size_known)
        self.position.write(write_version, dg)

        dg.add_bool(self.is_filled)
        self.placed.write(write_version, dg)
        dg.add_int32(self.omit_reason)

        dg.add_int32(len(self.reference_ids))

        for reference_id in self.reference_ids:
            write_pointer(dg, reference_id)

        dg.add_int32(len(self.texture_swap_ids))

        for texture_swap_id in self.texture_swap_ids:
            write_pointer(dg, texture_swap_id)

    def __str__(self):
        return 'TexturePlacement(texture_id={0}, group_id={1}, image_id={2}, dest_image_id={3}, has_uvs={4}, size_known={5}, position={6}, is_filled={7}, placed={8}, omit_reason={9}, reference_ids={10}, texture_swap_ids={11})'.format(
            self.texture_id,
            self.group_id,
            self.image_id,
            self.dest_image_id,
            self.has_uvs,
            self.size_known,
            self.position,
            self.is_filled,
            self.placed,
            self.omit_reason,
            self.reference_ids,
            self.texture_swap_ids
        )
