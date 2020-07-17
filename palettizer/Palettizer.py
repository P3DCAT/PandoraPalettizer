from panda3d.core import Filename, PNMImage
from .bam.BamFile import BamFile
from .PalettizeGlobals import *
from . import PalettizeUtils
import os

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""

class PalettizerException(Exception):
    pass

class Palettizer(object):

    def __init__(self, pandora_dir=None, maximum_size=2048, debug=True):
        self.set_pandora_dir(pandora_dir)
        self.maximum_size = maximum_size
        self.debug = debug

        self.boo_file = None

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

    def load_boo_file(self, filename):
        """
        Load a .boo file from the specified filename.
            :filename: The filename that points to the textures.boo file.
        """
        if self.boo_file is not None:
            # A .boo file is alerady loaded.
            return

        if not os.path.exists(filename):
            raise PalettizerException(f'Texture boo file at {filename} does not exist!')

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

        for palette_img in sorted(self.boo_file.get_objects_of_type('PaletteImage'), key=lambda img: (img.get_phase_num(), img.basename)):
            textures += f'Palette {palette_img.page.group.dirname}/maps/{palette_img.basename}jpg:\n'

            for placement in palette_img.placements:
                for source in placement.texture.sources:
                    textures += f'{source.filename}\n'

            textures += '\n'

        with open(filename, 'w') as f:
            f.write(self.boo_file.dump_objects())
            f.write(textures[:-1])

    def palettize_all_boo(self, jpg_output_dir, png_output_dir, save_png=True, save_jpg=True):
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

        for palette_img in self.boo_file.get_objects_of_type('PaletteImage'):
            new_image, alpha_image, has_alpha = self.palettize(palette_img, create_rgb=save_jpg)

            if save_png:
                self.write_png(new_image, has_alpha, png_output_dir, palette_img)
            if save_jpg:
                self.write_jpg(new_image, alpha_image, jpg_output_dir, palette_img)

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

            # Time to find the source file from Pandora!
            full_filename = os.path.abspath(os.path.join(self.maps_dir, source.filename))

            if not os.path.exists(full_filename):
                # We couldn't find the source file using the palettizer path.
                # Let's look in the entire Pandora folder!
                file_basename = os.path.basename(filename)
                full_filename = PalettizeUtils.search_for_file_in(self.pandora_dir, file_basename)

                if not full_filename:
                    # Well, it's not here...
                    raise PalettizerException(f'File does not exist in Pandora: {filename}')

            if self.debug:
                print(f'Reading {full_filename}...')

            # We've found the source file! Let's load it using Panda3D.
            img = PNMImage()
            img.read(Filename.from_os_specific(full_filename))

            if img.num_channels != 4:
                # We need an alpha channel no matter what, so if the image does not have one,
                # create an alpha channel, and fill it immediately with opaque pixels
                img.add_alpha()
                img.alpha_fill(1)

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
        new_x_size = PalettizeUtils.next_power_of_2(new_x_size)
        new_y_size = PalettizeUtils.next_power_of_2(new_y_size)

        # We will cut the resolution down one power until we reach our maximum size.
        while new_x_size > self.maximum_size or new_y_size > self.maximum_size:
            new_x_size //= 2
            new_y_size //= 2

        # We've changed the palette size. It is necessary to recalculate our texture distortion.
        x_distortion = new_x_size / current_x_size
        y_distortion = new_y_size / current_y_size

        # Create our palette image with four channels.
        # We will cut down the last channel when necessary.
        # Having a fourth, empty channel would only increase the file size.
        new_image = PNMImage(new_x_size, new_y_size, 4)

        # Textures with alpha always have four channels set (three for RGB and one for Alpha).
        has_alpha = palette_img.properties.effective_channels in (2, 4)
        alpha_image = None

        # If necessary and possible, create an alpha image as well.
        # Textures with alpha always have four channels set (three for RGB and one for Alpha).
        if create_rgb and has_alpha:
            alpha_image = PNMImage(new_x_size, new_y_size, 1)
            alpha_image.set_type(RGB_TYPE)

        for i, placement in enumerate(palette_img.placements):
            # Find the loaded source image from before...
            texture_img = imgs[i]

            # Calculate the placement of our image using the distortion!
            tex_position = placement.position
            tex_x_size = round(tex_position.x_size * x_distortion)
            tex_y_size = round(tex_position.y_size * y_distortion)
            tex_x = round(tex_position.x * x_distortion)
            tex_y = round(tex_position.y * y_distortion)

            if texture_img.get_x_size() != tex_x_size or texture_img.get_y_size() != tex_y_size:
                # Resize the image using Panda3D's quick filter algorithm, to fit our x_size and y_size.
                new_texture_img = PNMImage(tex_x_size, tex_y_size, texture_img.get_num_channels(), texture_img.get_maxval(), texture_img.get_type())
                new_texture_img.quick_filter_from(texture_img)
                texture_img = new_texture_img

            # If we've got an alpha image, copy the alpha values manually.
            if alpha_image:
                for i in range(tex_x_size):
                    for j in range(tex_y_size):
                        alpha_image.set_gray(tex_x + i, tex_y + j, texture_img.get_alpha(i, j))

            # Last step: copy our entire image over to the RGB image!
            new_image.copy_sub_image(texture_img, tex_x, tex_y, 0, 0, tex_x_size, tex_y_size)

        return new_image, alpha_image, has_alpha

    def write_png(self, new_image, has_alpha, folder, palette_img):
        """
        Saves a previously palettized image as a PNG file.
            :new_image: The palettized image containing RGB data.
            :has_alpha: Does this image contain alpha data?
            :folder: The folder to save the image in.
            :palette_img: The PaletteImage containing the palette data.
        """
        # Create the folder if necessary.
        folder = os.path.join(folder, palette_img.page.group.dirname, 'maps')

        if not os.path.exists(folder):
            os.makedirs(folder)

        palette_path = os.path.join(folder, palette_img.basename.strip('.'))

        if not has_alpha:
            # We do not have any alpha pixels, it would be wise to remove the alpha channel
            new_image.remove_alpha()

        new_image.write(Filename.from_os_specific(palette_path + '.png'))

    def write_jpg(self, new_image, alpha_image, folder, palette_img):
        """
        Saves a previously palettized image as a PNG file.
            :new_image: The palettized image containing RGB data.
            :alpha_image: The SGI variant of the palettized image containing alpha data.
            :folder: The folder to save the image in.
            :palette_img: The PaletteImage containing the palette data.
        """
        # Create the folder if necessary.
        folder = os.path.join(folder, palette_img.page.group.dirname, 'maps')

        if not os.path.exists(folder):
            os.makedirs(folder)

        palette_path = os.path.join(folder, palette_img.basename.strip('.'))

        # JPG files do not require alpha channels, so remove it.
        new_image.remove_alpha()
        new_image.write(Filename.from_os_specific(palette_path + '.jpg'))

        # Write our alpha file if it exists.
        if alpha_image is not None:
            alpha_image.write(Filename.from_os_specific(palette_path + '_a.rgb'))
