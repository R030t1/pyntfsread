import struct

class VolumeBootRecord(object):
    def __init__(self, data):
        self._data = data
        self.parse()
    
    def parse(self):
        self._end_of_sector = struct.unpack('<H', self._data[-2:])[0]
        if self._end_of_sector != 0xaa55:
            raise ValueError('End of sector marker is not 0xaa55')
        self._bytes_per_sector = struct.unpack('<H', self._data[0x0b:0x0d])[0]
        self._sectors_per_cluster = self._data[0x0D] # If negative, 2**n.
        self._mft_start = struct.unpack('<Q', self._data[0x30:0x38])[0] * \
            self._sectors_per_cluster * self._bytes_per_sector
        bprs = struct.unpack('<b', self._data[0x40:0x41])[0]
        if bprs < 0:
            self._bytes_per_record = 2**abs(bprs)
        else:
            self._bytes_per_record = bprs * self._sectors_per_cluster * \
                self._bytes_per_sector

class BIOSParameterBlock(object):
    pass

class ExtendedBIOSParameterBlock(object):
    pass

class MasterFileTable(object):
    def __init__(self, data):
        pass