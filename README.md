# Pandora Palettizer

Pandora Palettizer is a tool that can be used to automatically convert textures.boo files into FULL RESOLUTION palettes!

This tool is a very important cornerstone for the Toontown Texture Restoration Project.

The idea of this project is simple.

After all model files (EGG files) and textures are built in the Pandora/Spotify repository, egg-palettize leaves behind a textures.boo file.

It is extremely difficult to build the Pandora/Spotify repository, and as of yet, a comprehensive guide does not exist. Creating such a guide is out of the scope of this project.

This file contains very important palettization data that can be used to construct full resolution palettes!

The Panda3D egg-palettize tool cannot be used to create these full resolution palettes, as changing the palette size rearranges all textures inside the palette.

Since the Pandora leak is from 2010, it does not contain all textures from the 2013 build of the game. As such, some palettes might be missing textures. If a single texture is missing from a palette group, each palette image might be in the wrong order! Those palettes need to repaired manually using Photoshop.

Don't worry: when you run the program, it will list all textures used inside a single palette image! If a palette has to be repaired, this will greatly help with the manual texture lookup times.

* Use the `--jpg` flag to convert all palettes into JPG+RGB combo textures.
* Use the `--png` flag to convert all palettes into PNG textures.
* Use the `--all` flag to convert all palettes into both JPG+RGB and PNG textures.
* Use the `--dump` flag to dump the .boo file into a large file called `boo.txt`. This flag is most useful for developers.
* Use the `--skip-palette` flag to skip building palettes. If this flag is enabled, only stray textures will be built.
* Use the `--skip-stray` flag to skip building stray images. If this flag is enabled, only palettes will be built.
* Use the `--max-size` flag to set the maximum texture size. For example, `--max-size 2048` will not allow textures larger than 2048x2048 to be created. This is the default maximums size.
* Use the `--blur-amount` flag to set the amount of blurring used during texture resizing. When a texture is resized by Pandora Palettizer, it will be slightly blurred if necessary. Set this to 1.0 for default blurring behavior, and 0.0 to disable blurring altogether (which is faster, but yields ugly results).
* Use the `--boo` flag to specify the full path of the textures.boo file! For example: `--boo textures_backup.boo`
* Use the `--output` flag to specify the full path of the output directory. By default, this is the `built_palettes` directory.
* Use the `--texture-dir` flag to set your Spotify/Pandora directory. This is the directory that contains the `char`, `maps`, etc. directories.

## Installation

Your Python version must be at least 3.6, but newer versions are appreciated.

Make sure you've got Panda3D installed. The newer, the better.

You must clone the repository. This project has one dependency: `Pillow`, which can be installed using pip.

```
git clone https://github.com/P3DCAT/PandoraPalettizer
cd PandoraPalettizer
```

## Running

```
usage: python -m palettizer.Main [--jpg] [--png] [--all] [--dump] [--skip-palette]
               [--skip-stray] [--max-size MAX_SIZE]
               [--blur-amount BLUR_AMOUNT] [--boo BOO] [--output OUTPUT]
               [--texture-dir TEXTURE_DIR]

This script can be used to rebuild palettes from Pandora using the
textures.boo file.

optional arguments:
  -h, --help            show this help message and exit
  --jpg, -j             Convert palettes to JPG+RGB textures.
  --png, -p             Convert palettes to PNG textures.
  --all, -a             Convert palettes to both JPG+RGB and PNG textures.
  --dump, -d            Dump your textures.boo file into a boo.txt dump file.
  --skip-palette, -n    Skips the creation of palettes.
  --skip-stray, -m      Skips the creation of stray textures.
  --max-size MAX_SIZE, -s MAX_SIZE
                        The maximum size that a palettized texture can be,
                        measured in pixels.
  --blur-amount BLUR_AMOUNT, -x BLUR_AMOUNT
                        The amount of blur used during texture resizing. Set
                        this to 0 for no blurring. Default amount is 1.0.
  --boo BOO, -b BOO     Your textures.boo file, containing palettization data.
  --output OUTPUT, -o OUTPUT
                        Your output folder.
  --texture-dir TEXTURE_DIR, -i TEXTURE_DIR
                        The location of your Pandora/Spotify folder.
```

For example, to build all palettes and stray images from `C:\Data\Spotify`, building both JPG and PNG files, from the `textures.boo` file:

```
python -m palettizer.Main --jpg --png --texture-dir C:\Data\Spotify --boo textures.boo
```

To build only palettes from `C:\Data\Spotify`, building only JPG files, with a maximum size of `2048x2048` and regular blurring (1.0 amount):

```
python -m palettizer.Main --jpg --texture-dir C:\Data\Spotify --skip-palette --max-size 2048 --blur-amount 1.0
```

To dump the `textures.boo` file into a `boo.txt` file:

```
python -m palettizer.Main --dump --boo textures.boo
```

## Caveats

As mentioned before, Pandora does not contain all textures from the 2013 build of Toontown Online. Some palettes require repairation manually.

The Pandora/Spotify system is extremely difficult to build. You might need to procure a textures.boo file from somebody trustworthy.

You MUST run a manual optimization of all palettes after building the Pandora/Spotify repository! This will ensure that the palettes will take the same form and order as the 2010 Toontown Online palettes:

```
egg-palettize -af C:\Data\Spotify\maps\texture.txa --opt --all --egg
```