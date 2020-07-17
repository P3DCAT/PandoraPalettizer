from panda3d.core import Datagram, DatagramIterator

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""
class BamObject(object):

    def __init__(self, bam_file, bam_version):
        self.bam_file = bam_file
        self.bam_version = bam_version
        self.extra_data = b''

    def load_object(self, obj):
        dg = Datagram(obj['data'])
        di = DatagramIterator(dg)
        self.load(di)

        if di.get_remaining_size() > 0:
            self.extra_data = di.get_remaining_bytes()
            print('WARNING!!!!!! Extra data found: {}')

    def write_object(self, write_version, obj):
        dg = Datagram()
        self.write(write_version, dg)

        if self.extra_data:
            print('This is a', obj['handle_name'])
            print('WARNING!!!! Appending extra data {}'.format(self.extra_data))
            dg.append_data(self.extra_data)

        obj['data'] = dg.get_message()

    def load_type(self, type_constructor, di):
        obj = type_constructor(self.bam_file, self.bam_version)
        obj.load(di)
        return obj

    def load(self, di):
        pass

    def write(self, write_version, dg):
        pass
