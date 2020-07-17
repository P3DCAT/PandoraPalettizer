from .ClearedRegion import ClearedRegion
from .DestTextureImage import DestTextureImage
from .EggFile import EggFile
from .ImageFile import ImageFile
from .Matrix3F import Matrix3F
from .PaletteGroup import PaletteGroup
from .PaletteGroups import PaletteGroups
from .PaletteImage import PaletteImage
from .PalettePage import PalettePage
from .SourceTextureImage import SourceTextureImage
from .TextureImage import TextureImage
from .TexturePlacement import TexturePlacement
from .TexturePosition import TexturePosition
from .TextureProperties import TextureProperties
from .TextureReference import TextureReference

"""
  REPALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class BamFactory(object):

    def __init__(self):
        self.elements = {
            'ClearedRegion': ClearedRegion,
            'DestTextureImage': DestTextureImage,
            'EggFile': EggFile,
            'ImageFile': ImageFile,
            'Matrix3F': Matrix3F,
            'PaletteGroup': PaletteGroup,
            'PaletteGroups': PaletteGroups,
            'PaletteImage': PaletteImage,
            'PalettePage': PalettePage,
            'SourceTextureImage': SourceTextureImage,
            'TextureImage': TextureImage,
            'TexturePlacement': TexturePlacement,
            'TexturePosition': TexturePosition,
            'TextureProperties': TextureProperties,
            'TextureReference': TextureReference
        }

    def create(self, bam_file, handle_name, bam_version, base_name=None):
        if handle_name in self.elements:
            return self.elements[handle_name](bam_file, bam_version)
        if base_name in self.elements:
            return self.elements[base_name](bam_file, bam_version)
