from panda3d.core import LPoint2d
from .BamObject import BamObject
from .TextureProperties import TextureProperties
from .TextureGlobals import *
from .BamGlobals import *

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class TexturePosition(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    def get_uv_range(self):
        return self.max_uv - self.min_uv

    def load(self, di):
        self.margin = di.get_int32()
        self.x = di.get_int32()
        self.y = di.get_int32()
        self.x_size = di.get_int32()
        self.y_size = di.get_int32()
        self.min_uv = LPoint2d(di.get_float64(), di.get_float64())
        self.max_uv = LPoint2d(di.get_float64(), di.get_float64())
        self.wrap_u = di.get_int32()
        self.wrap_v = di.get_int32()

    def write(self, write_version, dg):
        dg.add_int32(self.margin)
        dg.add_int32(self.x)
        dg.add_int32(self.y)
        dg.add_int32(self.x_size)
        dg.add_int32(self.y_size)

        for uv in self.min_uv:
            dg.add_float64(uv)

        for uv in self.max_uv:
            dg.add_float64(uv)

        dg.add_int32(self.wrap_u)
        dg.add_int32(self.wrap_v)

    def __str__(self):
        return 'TexturePosition(margin={0}, x={1}, y={2}, x_size={3}, y_size={4}, min_uv={5}, max_uv={6}, wrap_u={7}, wrap_v={8}'.format(
            self.margin,
            self.x,
            self.y,
            self.x_size,
            self.y_size,
            self.min_uv,
            self.max_uv,
            get_wrap_mode_string(self.wrap_u),
            get_wrap_mode_string(self.wrap_v)
        )

    def __eq__(self, other):
        return self.margin == other.margin and self.x == other.x and self.y == other.y and self.x_size == other.x_size and self.y_size == other.y_size