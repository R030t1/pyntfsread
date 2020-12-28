#!/usr/bin/env python3
import sys, os
import vss, ntfs
import win32api, pywintypes, win32com.client
from pprint import pprint

def main() -> int:
    sc = vss.ShadowCopy('c')
    path = sc.shadow('c')
    print(path)
    f = open(path, 'rb')

    head, i = f.read(512), 1
    for b in head:
        print(f'{b:02x}',
            end=(' ' if i % 32 else '\n'))
        i += 1
    print()

    vbr = ntfs.VolumeBootRecord(head)
    f.seek(vbr._mft_start)
    mft = f.read(vbr._bytes_per_record)

    print(f'MFT start: {vbr._mft_start:x}')
    print(f'MFT record size: {vbr._bytes_per_record}')
    print()

    i = 1
    for b in mft:
        print(f'{b:02x}',
            end=(' ' if i % 32 else '\n'))
        i += 1


    f.close()
    sc.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())