from panda3d.core import Filename, PNMImage, LTexCoordd
from p3bamboo.BamFactory import BamFactory
from p3bamboo.BamFile import BamFile
from palettizer.bam import TextureGlobals
from palettizer import PalettizeGlobals, PalettizeUtils
import math, os

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""

SETUP_P3BAMBOO = False

def setup_p3bamboo():
    global SETUP_P3BAMBOO

    if SETUP_P3BAMBOO:
        return

    from palettizer.bam.ClearedRegion import ClearedRegion
    from palettizer.bam.DestTextureImage import DestTextureImage
    from palettizer.bam.EggFile import EggFile
    from palettizer.bam.ImageFile import ImageFile
    from palettizer.bam.Matrix3F import Matrix3F
    from palettizer.bam.PaletteGroup import PaletteGroup
    from palettizer.bam.PaletteGroups import PaletteGroups
    from palettizer.bam.PaletteImage import PaletteImage
    from palettizer.bam.PalettePage import PalettePage
    from palettizer.bam.SourceTextureImage import SourceTextureImage
    from palettizer.bam.TextureImage import TextureImage
    from palettizer.bam.TexturePlacement import TexturePlacement
    from palettizer.bam.TexturePosition import TexturePosition
    from palettizer.bam.TextureProperties import TextureProperties
    from palettizer.bam.TextureReference import TextureReference

    BamFactory.register_type('ClearedRegion', ClearedRegion)
    BamFactory.register_type('DestTextureImage', DestTextureImage)
    BamFactory.register_type('EggFile', EggFile)
    BamFactory.register_type('ImageFile', ImageFile)
    BamFactory.register_type('Matrix3F', Matrix3F)
    BamFactory.register_type('PaletteGroup', PaletteGroup)
    BamFactory.register_type('PaletteGroups', PaletteGroups)
    BamFactory.register_type('PaletteImage', PaletteImage)
    BamFactory.register_type('PalettePage', PalettePage)
    BamFactory.register_type('SourceTextureImage', SourceTextureImage)
    BamFactory.register_type('TextureImage', TextureImage)
    BamFactory.register_type('TexturePlacement', TexturePlacement)
    BamFactory.register_type('TexturePosition', TexturePosition)
    BamFactory.register_type('TextureProperties', TextureProperties)
    BamFactory.register_type('TextureReference', TextureReference)
    SETUP_P3BAMBOO = True

class PalettizerException(Exception):
    pass

class Palettizer(object):

    def __init__(self, pandora_dir=None, resize_strategy='round', resize_threshold=1.5, blur_amount=1.0, maximum_size=2048, debug=True):
        self.set_pandora_dir(pandora_dir)
        self.maximum_size = maximum_size
        self.resize_strategy = resize_strategy
        self.resize_threshold = resize_threshold
        self.blur_amount = blur_amount
        self.debug = debug

        self.boo_file = None

    def get_sorted_palette_imgs(self):
        """
        Returns all palette images from the loaded .boo file, sorted by phase number and name.
        """
        return sorted(self.boo_file.get_objects_of_type('PaletteImage'), key=lambda img: (img.get_phase_num(), img.basename))

    def get_texture_imgs(self):
        """
        Returns all texture images from the loaded .boo file.
        """
        return self.boo_file.get_objects_of_type('TextureImage')

    def set_pandora_dir(self, pandora_dir):
        """
        Set the directory containing all Pandora textures.
            :pandora_dir: The folder that contains all Pandora textures.
        """
        self.pandora_dir = pandora_dir

        if pandora_dir is None:
            self.maps_dir = None
        else:
            self.maps_dir = os.path.join(pandora_dir, 'maps')

    def find_texture(self, filename):
        """
        Finds any texture from the Pandora resources repository.
        Throws a PalettizerException if file could not be found.
            :filename: Relative filename that you are looking for.
        """
        full_filename = os.path.abspath(os.path.join(self.maps_dir, filename))

        if not os.path.exists(full_filename):
            # We couldn't find the file using the palettizer path.
            # Let's look in the entire Pandora folder!
            full_filename = PalettizeUtils.search_for_file_in(self.pandora_dir, os.path.basename(filename))

            if not full_filename:
                # Well, it's not here...
                raise PalettizerException(f'File does not exist in Pandora: {filename}')

        return full_filename

    def read_texture(self, filename):
        """
        Reads a texture from the Pandora resources repository.
        Returns a PNMImage object representing the image data.
        Throws a PalettizerException if file could not be found.
            :filename: Relative filename pointing to a texture file in the Pandora repository.
        """
        full_filename = self.find_texture(filename)

        if self.debug:
            print(f'Reading {full_filename}...')

        # We've found the source file! Let's load it using Panda3D.
        img = PNMImage()
        img.read(Filename.from_os_specific(full_filename))

        needs_alpha_fill = img.num_channels not in (2, 4)
        img.set_color_type(4)

        if needs_alpha_fill:
            # We need an alpha channel no matter what, so if the image does not have one,
            # it needs to be filled immediately with opaque pixels as it starts out with transparent pixels
            img.alpha_fill(1)

        return img

    def resize_image(self, image, x_size, y_size):
        """
        Resize an image using the Gaussian blur algorithm.
            :image: A PNMImage representing your image data.
            :x_size: The desired X size of the texture.
            :y_size: The desired Y size of the texture.
        """
        if image.get_x_size() == x_size and image.get_y_size() == y_size:
            # This image does not need to be resized!
            return image

        # Resize the image using Panda3D's gaussian filter algorithm, to fit our x_size and y_size.
        # WARNING! This blurs the image if too small!!! (Gaussian blur)
        new_image = PNMImage(x_size, y_size, image.get_num_channels(), image.get_maxval(), image.get_type())

        if self.blur_amount > 0:
            new_image.gaussian_filter_from(self.blur_amount, image)
        else:
            new_image.quick_filter_from(image)

        return new_image

    def scale_power_of_2(self, x_size, y_size):
        """
        Scales a texture's size to a nearby power of two,
        using this palettizer's preferred resize strategy and threshold.
            :x_size: The original X size of the texture.
            :y_size: The original Y size of the texture.
        """
        x_size = PalettizeUtils.get_power_of_2(x_size, self.resize_strategy, self.resize_threshold)
        y_size = PalettizeUtils.get_power_of_2(y_size, self.resize_strategy, self.resize_threshold)

        # We will cut the resolution down one power until we reach our maximum size.
        while x_size > self.maximum_size or y_size > self.maximum_size:
            x_size //= 2
            y_size //= 2

        return x_size, y_size

    def load_boo_file(self, filename):
        """
        Load a .boo file from the specified filename.
            :filename: The filename that points to the textures.boo file.
        """
        if self.boo_file is not None:
            # A .boo file is already loaded.
            return

        if not os.path.exists(filename):
            raise PalettizerException(f'Texture boo file at {filename} does not exist!')

        setup_p3bamboo()
        self.boo_file = BamFile()

        with open(filename, 'rb') as f:
            self.boo_file.load(f)

    def unload_boo_file(self):
        """
        Unload the currently loaded .boo file.
        """
        self.boo_file = None

    def dump_boo_to_text(self, filename):
        """
        Dump all contents of the loaded .boo file to a text file for further inspection.
            :filename: The filename that will store the text dump of the .boo file.
        """
        if self.debug:
            print(f'Dumping .boo file to {filename}...')

        textures = '\n'

        for palette_img in self.get_sorted_palette_imgs():
            textures += f'Palette {palette_img.page.group.dirname}/maps/{palette_img.basename}jpg:\n'

            for placement in palette_img.placements:
                for source in placement.texture.sources:
                    textures += f'{source.filename}\n'

            textures += '\n'

        with open(filename, 'w') as f:
            f.write(self.boo_file.dump_objects())
            f.write(textures[:-1])

    def palettize_all(self, jpg_output_dir, png_output_dir, save_png=True, save_jpg=True):
        """
        Palettize all palette images stored inside a BOO file.
            :jpg_output_dir: The directory your JPG+RGB files will be saved to.
            :png_output_dir: The directory your PNG files will be saved to.
            :save_png: Save PNG variants of the palette
            :save_jpg: Save JPG+RGB variants of the palette
        """
        if not self.boo_file:
            raise PalettizerException('No boo file loaded!')

        if not save_png and not save_jpg:
            raise PalettizerException('No action required.')

        for palette_img in self.get_sorted_palette_imgs():
            new_image, alpha_image, has_alpha, rgb_only = self.palettize(palette_img, create_rgb=save_jpg)
            phase_dir = palette_img.page.group.dirname

            if save_png:
                self.write_png(new_image, has_alpha, png_output_dir, phase_dir, palette_img.basename)
            if save_jpg:
                self.write_jpg(new_image, alpha_image, jpg_output_dir, phase_dir, palette_img.basename, rgb_only)

    def save_all_strays(self, jpg_output_dir, png_output_dir, save_png=True, save_jpg=True):
        """
        Save all stray images stored inside a BOO file.
            :jpg_output_dir: The directory your JPG+RGB files will be saved to.
            :png_output_dir: The directory your PNG files will be saved to.
            :save_png: Save PNG variants of the palette
            :save_jpg: Save JPG+RGB variants of the palette
        """
        if not self.boo_file:
            raise PalettizerException('No boo file loaded!')

        if not save_png and not save_jpg:
            raise PalettizerException('No action required.')

        for texture_img in self.get_texture_imgs():
            stray_texture = self.create_stray_texture(texture_img, create_rgb=save_jpg)

            if stray_texture is None:
                continue

            image, alpha_image, has_alpha, phase_folder, basename, rgb_only = stray_texture

            if save_png:
                self.write_png(image, has_alpha, png_output_dir, phase_folder, basename)
            if save_jpg:
                self.write_jpg(image, alpha_image, jpg_output_dir, phase_folder, basename, rgb_only)

    def create_stray_texture(self, texture_img, create_rgb=True):
        """
        Converts a TextureImage into actual PNMImages.
        Creates an RGB version of the texture if requested.
            :texture_img: The TextureImage you want to process.
            :create_rgb: Would you like to create an RGB variant of the texture? True by default.
        """
        if not texture_img.dest_ids:
            # This texture image is not a stray image.
            return

        source = texture_img.sources[0]
        dest = texture_img.dests[0]

        # Extrapolate the phase folder from the first assigned group
        phase_folder = texture_img.actual_assigned_groups.groups[0].dirname

        # Extrapolate the base name from the destination image
        basename = os.path.splitext(os.path.basename(dest.filename))[0]

        # Is this an RGB only texture?
        # Some textures, like fonts, are saved as grayscale RGB.
        rgb_only = texture_img.properties.format == TextureGlobals.F_alpha

        # Read the texture from Pandora!
        image = self.read_texture(source.filename)

        # Let's save the texture as a power of two resolution.
        x_size, y_size = self.scale_power_of_2(image.get_x_size(), image.get_y_size())

        alpha_image = None

        # Resize our image to the desired size.
        image = self.resize_image(image, x_size, y_size)
        has_alpha = source.properties.effective_channels in (2, 4)

        if dest.alpha_filename and has_alpha and create_rgb and not rgb_only:
            alpha_image = PNMImage(x_size, y_size, 1)
            alpha_image.set_type(PalettizeGlobals.RGB_TYPE)

            # Copy alpha channel from source image
            for i in range(x_size):
                for j in range(y_size):
                    alpha_image.set_gray(i, j, image.get_alpha(i, j))

        return image, alpha_image, has_alpha, phase_folder, basename, rgb_only

    def palettize(self, palette_img, create_rgb=True):
        """
        Runs all palettization procedures on the given PaletteImage.
        Creates an RGB version of the palette if requested.
            :palette_img: The PaletteImage you want to palettize.
            :create_rgb: Would you like to create an RGB variant of the palette? True by default.
        """
        # We need to know the palette's prior size
        if not palette_img.size_known:
            raise PalettizerException("Palette image's size is not known, this is a fatal error!")

        palette_name = palette_img.basename

        if self.debug:
            print(f'[{palette_img.page.group.dirname}] Compiling {palette_name}..')

        # Our max distortion is 1, as we do not want to resize the palette to be smaller accidentally
        max_distortion = 1

        # This array holds all of our PNMImage source textures
        imgs = []

        # We're going to check all of the source textures
        # so that we can load all of them and determine our palette's final size
        for placement in palette_img.placements:
            sources = placement.texture.sources

            # We need to know the size of all source textures
            # If a source texture's size is not known, that means that it has been defined but did not exist on the disk when creating textures.boo
            for source in sources:
                if not source.size_known:
                    print(f'Warning: Size is not known for source {source.filename}, please consider fixing the texture path and re-running egg-palettize')

            # Source (original) full resolution texture size
            source = sources[0]
            x_size = source.x_size
            y_size = source.y_size

            # Prior texture position and size
            tex_position = placement.position
            tex_x_size = tex_position.x_size
            tex_y_size = tex_position.y_size

            # DISTORTER
            # Fold the points until they scream out
            # DISTORTER
            # Change the way it sounds

            # We need to calculate the maximum distortion for both our X and Y (U/V) coordinates
            if x_size != tex_x_size:
                x_distortion = x_size / tex_x_size

                if x_distortion > max_distortion:
                    max_distortion = x_distortion

            if y_size != tex_y_size:
                y_distortion = y_size / tex_y_size

                if y_distortion > max_distortion:
                    max_distortion = y_distortion

            # If we have more than one source, that means our texture
            # has been defined multiple times for the same group...
            # Panda3D uses the first source texture only, so that's what we'll do.
            # But we'll make sure to print a warning either way!
            if len(sources) > 1:
                source2 = sources[1]

                if source2.x_size != x_size or source2.y_size != y_size:
                    print(f'Two different source textures are defined for {palette_name}: {source.filename} ({x_size} {y_size}) vs {source2.filename} ({source2.x_size} {source2.y_size})')

            # Time to load the source file from Pandora!
            img = self.read_texture(source.filename)

            # Add the source image to our list
            imgs.append(img)

        # Well, time to calculate the palette's final size!
        # We will multiply the current size with the highest distortion.
        # We do NOT calculate X and Y distortion separately.
        # Doing so would destroy the aspect ratio of the palette.
        current_x_size = palette_img.x_size
        current_y_size = palette_img.y_size
        new_x_size = round(current_x_size * max_distortion)
        new_y_size = round(current_y_size * max_distortion)

        # Power of two time!
        # It's easier for the game engine to load, as it does not have to scale it automatically.
        new_x_size, new_y_size = self.scale_power_of_2(new_x_size, new_y_size)

        # We've changed the palette size. It is necessary to recalculate our texture distortion.
        x_distortion = new_x_size / current_x_size
        y_distortion = new_y_size / current_y_size

        # Create our palette image with four channels.
        # We will cut down the last channel when necessary.
        # Having a fourth, empty channel would only increase the file size.
        new_image = PNMImage(new_x_size, new_y_size, 4)
        new_image.alpha_fill(1)

        # Textures with alpha always have four channels set (three for RGB and one for Alpha).
        has_alpha = palette_img.properties.effective_channels in (2, 4)
        rgb_only = palette_img.properties.format == TextureGlobals.F_alpha
        alpha_image = None

        # If necessary and possible, create an alpha image as well.
        # Textures with alpha always have four channels set (three for RGB and one for Alpha).
        if create_rgb and has_alpha and not rgb_only:
            alpha_image = PNMImage(new_x_size, new_y_size, 1)
            alpha_image.set_type(PalettizeGlobals.RGB_TYPE)

        for i, placement in enumerate(palette_img.placements):
            # Find the loaded source image from before...
            texture_img = imgs[i]

            # Calculate the placement of our image!
            tex_position = placement.placed

            # Determine the upper left and lower right corners
            # with some matrix magic.
            transform = placement.compute_tex_matrix()
            ul = transform.xform_point(LTexCoordd(0.0, 1.0))
            lr = transform.xform_point(LTexCoordd(1.0, 0.0))

            # Calculate the top, left, bottom and right corners.
            top = int(math.floor((1.0 - ul[1]) * new_y_size + 0.5))
            left = int(math.floor(ul[0] * new_x_size + 0.5))
            bottom = int(math.floor((1.0 - lr[1]) * new_y_size + 0.5))
            right = int(math.floor(lr[0] * new_x_size + 0.5))

            tex_x_size = right - left
            tex_y_size = bottom - top
            org_x_size = round(tex_position.x_size * x_distortion)
            org_y_size = round(tex_position.y_size * y_distortion)
            tex_x = round(tex_position.x * x_distortion)
            tex_y = round(tex_position.y * y_distortion)

            # Resize our image to the desired size.
            texture_img = self.resize_image(texture_img, tex_x_size, tex_y_size)

            for y in range(tex_y, tex_y + org_y_size):
                sy = y - top

                # UV wrapping modes - V component (for Y texture coordinate)
                if placement.placed.wrap_v == TextureGlobals.WM_clamp:
                    sy = max(min(sy, tex_y_size - 1), 0)
                elif placement.placed.wrap_v == TextureGlobals.WM_mirror:
                    sy = (tex_y_size * 2) - 1 - ((-sy - 1) % (tex_y_size * 2)) if sy < 0 else sy % (tex_y_size * 2)
                    sy = sy if sy < tex_y_size else 2 * tex_y_size - sy - 1
                elif placement.placed.wrap_v == TextureGlobals.WM_mirror_once:
                    sy = sy if sy < tex_y_size else 2 * tex_y_size - sy - 1

                    # Repeat texture
                    sy = tex_y_size - 1 - ((-sy - 1) % tex_y_size) if sy < 0 else sy % tex_y_size
                elif placement.placed.wrap_v == TextureGlobals.WM_border_color:
                    if sy < 0 or sy >= tex_y_size:
                        continue
                else:
                    # Repeat texture
                    sy = tex_y_size - 1 - ((-sy - 1) % tex_y_size) if sy < 0 else sy % tex_y_size

                for x in range(tex_x, tex_x + org_x_size):
                    sx = x - left

                    # UV wrapping modes - U component (for X texture coordinate)
                    if placement.placed.wrap_u == TextureGlobals.WM_clamp:
                        sx = max(min(sx, tex_x_size - 1), 0)
                    elif placement.placed.wrap_u == TextureGlobals.WM_mirror:
                        sx = (tex_x_size * 2) - 1 - ((-sx - 1) % (tex_x_size * 2)) if sx < 0 else sx % (tex_x_size * 2)
                        sx = sx if sx < tex_x_size else 2 * tex_x_size - sx - 1
                    elif placement.placed.wrap_u == TextureGlobals.WM_mirror_once:
                        sx = sx if sx >= 0 else ~sx

                        # Repeat texture
                        sx = tex_x_size - 1 - ((-sx - 1) % tex_x_size) if sx < 0 else sx % tex_x_size
                    elif placement.placed.wrap_u == TextureGlobals.WM_border_color:
                        if sx < 0 or sx >= tex_x_size:
                            continue
                    else:
                        # Repeat texture
                        sx = tex_x_size - 1 - ((-sx - 1) % tex_x_size) if sx < 0 else sx % tex_x_size

                    new_image.set_xel(x, y, texture_img.get_xel(sx, sy))
                    new_image.set_alpha(x, y, texture_img.get_alpha(sx, sy))

                    if alpha_image:
                        alpha_image.set_gray(x, y, texture_img.get_alpha(sx, sy))

        return new_image, alpha_image, has_alpha, rgb_only

    def write_png(self, new_image, has_alpha, folder, phase_dir, basename):
        """
        Saves a previously palettized image as a PNG file.
            :new_image: The palettized image containing RGB data.
            :has_alpha: Does this image contain alpha data?
            :folder: The folder to save the image in.
            :phase_dir: The name of the phase folder containing the texture, for example: "phase_3"
            :basename: The filename of the image, for example: "avatar_palette_1mla_1"
        """
        # Create the folder if necessary.
        folder = os.path.join(folder, phase_dir, 'maps')

        if not os.path.exists(folder):
            os.makedirs(folder)

        palette_path = os.path.join(folder, basename.strip('.'))

        if not has_alpha:
            # We do not have any alpha pixels, it would be wise to remove the alpha channel
            new_image.remove_alpha()

        new_image.write(Filename.from_os_specific(f'{palette_path}.png'))

    def write_jpg(self, new_image, alpha_image, folder, phase_dir, basename, rgb_only=False):
        """
        Saves a previously palettized image as a PNG file.
            :new_image: The palettized image containing RGB data.
            :alpha_image: The SGI variant of the palettized image containing alpha data.
            :folder: The folder to save the image in.
            :phase_dir: The name of the phase folder containing the texture, for example: "phase_3"
            :basename: The filename of the image, for example: "avatar_palette_1mla_1"
            :rgb_only: True if we only want to save the RGB variant of this image.
        """
        # Create the folder if necessary.
        folder = os.path.join(folder, phase_dir, 'maps')

        if not os.path.exists(folder):
            os.makedirs(folder)

        palette_path = os.path.join(folder, basename.strip('.'))

        # We have an RGB only file!
        if rgb_only:
            new_image.write(Filename.from_os_specific(f'{palette_path}.rgb'))
            return

        # JPG files do not require alpha channels, so remove it.
        new_image.remove_alpha()
        new_image.write(Filename.from_os_specific(f'{palette_path}.jpg'))

        # Write our alpha file if it exists.
        if alpha_image is not None:
            alpha_image.write(Filename.from_os_specific(f'{palette_path}_a.rgb'))
