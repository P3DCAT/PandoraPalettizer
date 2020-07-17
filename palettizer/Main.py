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

    palettizer = Palettizer()

    if args.dump:
        palettizer.load_boo_file(args.boo)
        palettizer.dump_boo_to_text('boo.txt')

    jpg = args.all or args.jpg
    png = args.all or args.png

    if not jpg and not png:
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

    palettizer.set_pandora_dir(args.texture_dir)
    palettizer.load_boo_file(args.boo)
    palettizer.palettize_all_boo(
        jpg_output_dir=os.path.join(args.output, 'jpg'),
        png_output_dir=os.path.join(args.output, 'png'),
        save_png=png,
        save_jpg=jpg
    )

if __name__ == '__main__':
    main()