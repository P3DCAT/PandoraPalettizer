from .bam.BamFile import BamFile

"""
  REPALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""

# Working copy
def main():
    bam = BamFile()

    with open('C:\\Users\\User\\Desktop\\New folder (2)\\textures.boo', 'rb') as f:
        bam.load(f)

    with open('boo.txt', 'w') as f:
        f.write(bam.dump_objects())

    all_handles = []
    page_ids = bam.find_related('PaletteImage')

    for obj_id, obj in bam.objects.items():
        if obj['handle_id'] not in page_ids:
            continue

        node = bam.bam_factory.create(bam, obj['handle_name'], bam_version=bam.version)
        node.load_object(obj)
        break

if __name__ == '__main__':
    main()