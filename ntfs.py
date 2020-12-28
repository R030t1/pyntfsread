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

# File record:
#
#    MULTI_SECTOR_HEADER
# uchar[4]  Signature
# ushort    UpdateSequenceArrayOffset
# ushort    UpdateSequenceArraySize
#
#    FILE_REFERENCE
# ulong     Low
# ushort    High
# ushort    Sequence
#
#    UPDATE_SEQUENCE_ARRAY
#
#
#    FILE_RECORD_SEGMENT_HEADER
# multi_sector_header
# ulonglong Reserved
# ushort    SequenceNumber
# ushort    Reserved
# ushort    FirstAttributeOffset
# ushort    Flags
# ulong[2]  Reserved
# file_reference
# ushort    Reserved
# update_sequence_array
#
#    ATTRIBUTE_RECORD_HEADER
# attribute_type_code
# ulong     RecordLength
# uchar     FormCode
# uchar     NameLength
# ushort    NameOffset
# ushort    Flags
# ushort    Instance
# union {
#   struct {
# ulong     ValueLength
# ushort    ValueOffset
# uchar[2]  Reserved
#   } Resident
#   struct {
# vcn       LowestVcn
# vcn       HighestVcn
# ushort    MappingPairsOffset
# uchar[6]  Reserved
# longlong  AllocatedLength
# longlong  FileSize
# longlong  ValidDataLength
# longlong  TotalAllocated
#   } Nonresident
# }
#
#    ATTRIBUTE_LIST_ENTRY
# attribute_type_code
# ushort    RecordLength
# uchar     AttributeNameLength
# uchar     AttributeNameOffset
# vcn       LowestVcn
# mft_segment
