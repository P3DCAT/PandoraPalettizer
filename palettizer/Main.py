from .Palettizer import Palettizer
import argparse, os

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""

def main():
    parser = argparse.ArgumentParser(description='This script can be used to rebuild palettes from Pandora using the textures.boo file.')
    parser.add_argument('--jpg', '-j', action='store_true', help='Convert palettes to JPG+RGB textures.')
    parser.add_argument('--png', '-p', action='store_true', help='Convert palettes to PNG textures.')
    parser.add_argument('--all', '-a', action='store_true', help='Convert palettes to both JPG+RGB and PNG textures.')
    parser.add_argument('--dump', '-d', action='store_true', help='Dump your textures.boo file into a boo.txt dump file.')
    parser.add_argument('--skip-palette', '-n', action='store_true', help='Skips the creation of palettes.')
    parser.add_argument('--skip-stray', '-m', action='store_true', help='Skips the creation of stray textures.')
    parser.add_argument('--max-size', '-s', type=int, default=2048, help='The maximum size that a palettized texture can be, measured in pixels.')
    parser.add_argument('--blur-amount', '-x', type=float, default=1.0, help='The amount of blur used during texture resizing. Set this to 0 for no blurring. Default amount is 1.0.')
    parser.add_argument('--boo', '-b', help='Your textures.boo file, containing palettization data.')
    parser.add_argument('--output', '-o', help='Your output folder.')
    parser.add_argument('--texture-dir', '-i', help='The location of your Pandora/Spotify folder.')
    args = parser.parse_args()

    # Priorities:
    # 1. --boo argument
    # 2. textures.boo in working directory
    # 3. textures.boo in Pandora maps directory
    if not args.boo:
        if os.path.exists('textures.boo'):
            args.boo = os.path.abspath('textures.boo')
        elif args.texture_dir:
            args.boo = os.path.join(args.texture_dir, 'maps', 'textures.boo')

    if not os.path.exists(args.boo):
        print(f'{args.boo} does not exist!')
        return

    palettizer = Palettizer(blur_amount=args.blur_amount, maximum_size=args.max_size)

    if args.dump:
        palettizer.load_boo_file(args.boo)
        palettizer.dump_boo_to_text('boo.txt')

    save_jpg = args.all or args.jpg
    save_png = args.all or args.png

    if (not save_jpg and not save_png) or (args.skip_palette and args.skip_stray):
        if not args.dump:
            parser.print_help()
            print('Nothing to do. Are you sure you did not forget --all?')

        return

    if not args.output:
        # Default output folder name
        args.output = os.path.abspath('built_palettes')

    if not args.texture_dir:
        parser.print_help()
        print('The following arguments are required: texture-dir')
        return

    if not os.path.exists(args.texture_dir):
        print('Pandora directory does not exist!')
        return

    map_folder = os.path.join(args.texture_dir, 'maps')

    if not os.path.exists(map_folder):
        print('There is no maps folder in your Pandora directory!')
        return

    jpg_output_dir = os.path.join(args.output, 'jpg')
    png_output_dir = os.path.join(args.output, 'png')

    if args.max_size < 64:
        print('Maximum texture size is too small! Try at least 64x64!')
        return

    palettizer.set_pandora_dir(args.texture_dir)
    palettizer.load_boo_file(args.boo)

    if not args.skip_palette:
        palettizer.palettize_all(jpg_output_dir, png_output_dir, save_jpg, save_png)

    if not args.skip_stray:
        palettizer.save_all_strays(jpg_output_dir, png_output_dir, save_jpg, save_png)

if __name__ == '__main__':
    main()