from .BamObject import BamObject
from .TextureGlobals import *
from .BamGlobals import *

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class TextureProperties(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    def load(self, di):
        self.got_num_channels = di.get_bool()
        self.num_channels = di.get_int32()

        if PI_VERSION >= 9:
            self.effective_channels = di.get_int32()
        else:
            self.effective_channels = num_channels

        self.format = di.get_int32()
        self.force_format = di.get_bool()

        if PI_VERSION >= 9:
            self.generic_format = di.get_bool()
        else:
            self.generic_format = False

        if PI_VERSION >= 13:
            self.keep_format = di.get_bool()
        else:
            self.keep_format = False

        self.minfilter = di.get_int32()
        self.magfilter = di.get_int32()

        if PI_VERSION >= 18:
            self.quality_level = di.get_int32()
        else:
            self.quality_level = QL_unspecified

        self.anisotropic_degree = di.get_int32()

        self.color_type_id = read_pointer(di)
        self.alpha_type_id = read_pointer(di)

    def write(self, write_version, dg):
        dg.add_bool(self.got_num_channels)
        dg.add_int32(self.num_channels)

        if PI_VERSION >= 9:
            dg.add_int32(self.effective_channels)

        dg.add_int32(self.format)
        dg.add_bool(self.force_format)

        if PI_VERSION >= 9:
            dg.add_bool(self.generic_format)

        if PI_VERSION >= 13:
            dg.add_bool(self.keep_format)

        dg.add_int32(self.minfilter)
        dg.add_int32(self.magfilter)

        if PI_VERSION >= 18:
            dg.add_int32(self.quality_level)

        dg.add_int32(self.anisotropic_degree)

        write_pointer(dg, self.color_type_id)
        write_pointer(dg, self.alpha_type_id)

    def get_type_string(self):
        if not self.color_type_id:
            return 'none'
        if self.alpha_type_id:
            return 'alpha'
        return 'color'

    def __str__(self):
        return 'TextureProperties(got_channels={0}, effective_channels={1}, force_format={2}, generic_format={3}, keep_format={4}, format={5}, minfilter={6}, magfilter={7}, anisotropic_degree={8}, type={9}, quality={10})'.format(
            self.got_num_channels,
            self.effective_channels,
            self.force_format,
            self.generic_format,
            self.keep_format,
            get_format_string(self.format),
            get_filter_string(self.minfilter),
            get_filter_string(self.magfilter),
            self.anisotropic_degree,
            self.get_type_string(),
            get_quality_string(self.quality_level)
        )