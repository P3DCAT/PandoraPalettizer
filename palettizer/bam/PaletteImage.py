from p3bamboo.BamObject import BamObject
from palettizer.bam.ImageFile import ImageFile
from palettizer.bam.ClearedRegion import ClearedRegion

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class PaletteImage(ImageFile):

    def __init__(self, bam_file, bam_version):
        ImageFile.__init__(self, bam_file, bam_version)

    @property
    def placements(self):
        return [self.bam_file.get_object(placement_id) for placement_id in self.placement_ids]

    @property
    def page(self):
        return self.bam_file.get_object(self.page_id)

    def get_phase_num(self):
        phase = self.page.group.dirname

        try:
            return float(phase.split('_')[-1])
        except:
            return -1

    def load(self, di):
        ImageFile.load(self, di)

        num_cleared_regions = di.get_uint32()
        self.cleared_regions = [self.load_type(ClearedRegion, di) for i in range(num_cleared_regions)]

        self.placement_ids = self.bam_file.read_pointer_uint32_list(di) # TexturePlacement

        self.page_id = self.bam_file.read_pointer(di) # PalettePage
        self.index = di.get_uint32()
        self.basename = di.get_string()
        self.new_image = di.get_bool()

    def write(self, write_version, dg):
        ImageFile.write(self, write_version, dg)

        dg.add_uint32(len(self.cleared_regions))

        for region in self.cleared_regions:
            region.write(write_version, dg)

        self.bam_file.write_pointer_uint32_list(dg, self.placement_ids)

        self.bam_file.write_pointer(dg, self.page_id)
        dg.add_uint32(self.index)
        dg.add_string(self.basename)
        dg.add_bool(self.new_image)

    def __str__(self):
        return 'PaletteImage(parent={0}, cleared_regions={1}, placement_ids={2}, page_id={3}, index={4}, basename={5}, new_image={6})'.format(
            super(PaletteImage, self).__str__(),
            ', '.join([str(region) for region in self.cleared_regions]),
            self.placement_ids,
            self.page_id,
            self.index,
            self.basename,
            self.new_image
        )
