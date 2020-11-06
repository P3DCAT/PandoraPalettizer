from panda3d.core import PNMFileTypeRegistry

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""

PI_VERSION = 20
RGB_TYPE = PNMFileTypeRegistry.get_global_ptr().get_type_from_extension('.rgb')
