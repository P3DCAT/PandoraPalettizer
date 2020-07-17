from .BamObject import BamObject
from .ImageFile import ImageFile
from .PaletteGroups import PaletteGroups
from .BamGlobals import *
from .TextureGlobals import *

"""
  REPALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class TextureImage(ImageFile):

    def __init__(self, bam_file, bam_version):
        ImageFile.__init__(self, bam_file, bam_version)

    @property
    def placements(self):
        return [self.bam_file.get_object(placement_id) for placement_id in self.placement_ids]

    @property
    def sources(self):
        return [self.bam_file.get_object(source_id) for source_id in self.source_ids]

    @property
    def dests(self):
        return [self.bam_file.get_object(dest_id) for dest_id in self.dest_ids]

    def load(self, di):
        ImageFile.load(self, di)
        self.name = di.get_string()
        self.is_surprise = di.get_bool()
        self.ever_read_image = di.get_bool()
        self.forced_grayscale = di.get_bool()
        self.alpha_bits = di.get_uint8()
        self.alpha_mode = di.get_int16()

        if PI_VERSION >= 16:
            self.mid_pixel_ratio = di.get_float64()
            self.is_cutout = di.get_bool()
        else:
            self.ever_read_image = False
            self.mid_pixel_ratio = 0.0
            self.is_cutout = False

        if PI_VERSION >= 17:
            self.txa_wrap_u = di.get_uint8()
            self.txa_wrap_v = di.get_uint8()
        else:
            self.txa_wrap_u = WM_unspecified
            self.txa_wrap_v = WM_unspecified

        self.actual_assigned_groups = self.load_type(PaletteGroups, di)

        num_placements = di.get_uint32()
        self.placement_ids = [read_pointer(di) for i in range(num_placements * 2)] # TexturePlacement

        num_sources = di.get_uint32()
        self.source_ids = [read_pointer(di) for i in range(num_sources)] # SourceTextureImage

        num_dests = di.get_uint32()
        self.dest_ids = [read_pointer(di) for i in range(num_dests)] # DestTextureImage

    def write(self, write_version, dg):
        ImageFile.write(self, di)
        dg.add_string(self.name)
        dg.add_bool(self.is_surprise)
        dg.add_bool(self.ever_read_image)
        dg.add_bool(self.forced_grayscale)
        dg.add_uint8(self.alpha_bits)
        dg.add_int16(self.alpha_mode)

        if PI_VERSION >= 16:
            dg.add_float64(self.mid_pixel_ratio)
            dg.add_bool(self.is_cutout)

        if PI_VERSION >= 17:
            dg.add_uint8(self.txa_wrap_u)
            dg.add_uint8(self.txa_wrap_v)

        self.actual_assigned_groups.write(write_version, dg)

        dg.add_uint32(len(self.placement_ids) // 2)

        for placement_id in self.placement_ids:
            write_pointer(dg, placement_id)

        dg.add_uint32(len(self.source_ids))

        for source_id in self.source_ids:
            write_pointer(dg, source_id)

        dg.add_uint32(len(self.dest_ids))

        for dest_id in self.dest_ids:
            write_pointer(dg, dest_id)

    def __str__(self):
        return 'TextureImage(parent={0}, name={1}, is_surprise={2}, ever_read_image={3}, forced_grayscale={4}, alpha_bits={5}, alpha_mode={6}, mid_pixel_ratio={7}, is_cutout={8}, txa_wrap_u={9}, txa_wrap_v={10}, actual_assigned_groups={11}, placement_ids={12}, source_ids={13}, dest_ids={14}'.format(
            super(TextureImage, self).__str__(),
            self.name,
            self.is_surprise,
            self.ever_read_image,
            self.forced_grayscale,
            self.alpha_bits,
            get_alpha_mode_string(self.alpha_mode),
            self.mid_pixel_ratio,
            self.is_cutout,
            get_wrap_mode_string(self.txa_wrap_u),
            get_wrap_mode_string(self.txa_wrap_v),
            self.actual_assigned_groups,
            self.placement_ids,
            self.source_ids,
            self.dest_ids
        )