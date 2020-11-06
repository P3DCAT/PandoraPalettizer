from p3bamboo.BamObject import BamObject

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class ClearedRegion(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    def load(self, di):
        BamObject.load(self, di)

        self.x = di.get_int32()
        self.y = di.get_int32()
        self.x_size = di.get_int32()
        self.y_size = di.get_int32()

    def write(self, write_version, dg):
        BamObject.write(self, write_version, dg)

        dg.add_int32(self.x)
        dg.add_int32(self.y)
        dg.add_int32(self.x_size)
        dg.add_int32(self.y_size)

    def __str__(self):
        return 'ClearedRegion(x={0}, y={1}, x_size={2}, y_size={3}'.format(
            self.x,
            self.y,
            self.x_size,
            self.y_size
        )
