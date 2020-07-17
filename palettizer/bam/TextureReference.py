from .BamObject import BamObject
from .Matrix3F import Matrix3F
from .TextureProperties import TextureProperties
from .TextureGlobals import *
from .BamGlobals import *

"""
  REPALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class TextureReference(BamObject):

    def __init__(self, bam_file, bam_version):
        BamObject.__init__(self, bam_file, bam_version)

    @property
    def egg_file(self):
        return self.bam_file.get_object(self.egg_file_id)

    @property
    def source_texture(self):
        return self.bam_file.get_object(self.source_texture_id)

    @property
    def placement(self):
        return self.bam_file.get_object(self.placement_id)

    def load(self, di):
        self.egg_file_id = read_pointer(di)

        self.tref_name = di.get_string()

        self.tex_mat = self.load_type(Matrix3F, di)
        self.inv_tex_mat = self.load_type(Matrix3F, di)

        self.source_texture_id = read_pointer(di) # SourceTextureImage
        self.placement_id = read_pointer(di) # TexturePlacement

        self.uses_alpha = di.get_bool()
        self.any_uvs = di.get_bool()
        self.min_uv = [di.get_float64(), di.get_float64()]
        self.max_uv = [di.get_float64(), di.get_float64()]
        self.wrap_u = di.get_int32()
        self.wrap_v = di.get_int32()
        self.properties = self.load_type(TextureProperties, di)

    def write(self, write_version, dg):
        write_pointer(dg, self.egg_file_id)

        dg.add_string(self.tref_name)

        self.tex_mat.write(write_version, dg)
        self.inv_tex_mat.write(write_version, dg)

        write_pointer(dg, self.source_texture_id)
        write_pointer(dg, self.placement_id)

        dg.add_bool(self.uses_alpha)
        dg.add_bool(self.any_uvs)

        for uv in self.min_uv:
            dg.add_float64(uv)

        for uv in self.max_uv:
            dg.add_float64(uv)

        dg.add_int32(self.wrap_u)
        dg.add_int32(self.wrap_v)

        self.properties.write(write_version, dg)

    def __str__(self):
        return 'TextureReference(egg_file_id={0}, tref_name={1}, tex_mat={2}, inv_tex_mat={3}, uses_alpha={4}, any_uvs={5}, min_uv={6}, max_uv={7}, wrap_u={8}, wrap_v={9}, properties={10}'.format(
            self.egg_file_id,
            self.tref_name,
            self.tex_mat,
            self.inv_tex_mat,
            self.uses_alpha,
            self.any_uvs,
            self.min_uv,
            self.max_uv,
            get_wrap_mode_string(self.wrap_u),
            get_wrap_mode_string(self.wrap_v),
            self.properties
        )