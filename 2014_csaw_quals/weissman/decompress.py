import sys
import struct
from collections import defaultdict
import os

def print_info(code, decomp, data, idx):
    pass
    print 'code: %x' % (code)
    print 'idx: %x' % (idx)
    print 'bytes: %04x' % (struct.unpack('<H', str(data[idx+1:idx+3]))[0])
    print 'offset: %x' % len(decomp)
    print 'prev: %s' % (str(decomp[len(decomp) - 9*3:]).replace('\n', '\\n').replace('\r', '\\r'))
    print 'next: %x' % (data[idx+3])
    print ''

def main():
    with open(sys.argv[1], 'rb') as f:
        data = bytearray(f.read())

    idx = 0
    entry_idx = 0

    decomp = bytearray()
    codes = defaultdict(int)
    byte_vals = defaultdict(int)

    while idx < len(data):
        code = data[idx]
        codes[data[idx]] += 1
        if code == 0x13:
            entry = data[idx+1:idx+10]
            decomp.extend(entry)
            entry_idx += 1
            idx += 10
        elif code == 0x8:
            print_info(code, decomp, data, idx)
            decomp.extend('\x00'*4)
            byte_vals[str(data[idx+1:idx+3])] += 1
            idx += 3
        elif code == 0xa:
            print_info(code, decomp, data, idx)
            decomp.extend('\x00'*5)
            byte_vals[str(data[idx+1:idx+3])] += 1
            idx += 3
        elif code == 0xc:
            print_info(code, decomp, data, idx)
            byte_vals[str(data[idx+1:idx+3])] += 1
            decomp.extend('\x00'*6)
            idx += 3
        elif code == 0xe:
            print_info(code, decomp, data, idx)
            byte_vals[str(data[idx+1:idx+3])] += 1
            decomp.extend('\x00'*7)
            idx += 3
        elif code == 0x10:
            print_info(code, decomp, data, idx)
            byte_vals[str(data[idx+1:idx+3])] += 1
            decomp.extend('\x00'*8)
            idx += 3
        elif code == 0x12:
            print_info(code, decomp, data, idx)
            byte_vals[str(data[idx+1:idx+3])] += 1
            decomp.extend('\x00'*9)
            idx += 3
        else:
            print idx
            print 'Arr, I don\'t know what I\'m doing...'
            quit()

    with open('%s_decomp%s' % (os.path.splitext(sys.argv[1])[0],
                               os.path.splitext(sys.argv[1])[1]), 'wb') as o:
        o.write(str(decomp))

    for k in codes.keys():
        print '%x: %s' % (k, codes[k])

    print '\nByte vals %s:' % (len(byte_vals))
    for k in sorted(byte_vals.keys()):
        print '%04x: %s' % (struct.unpack('<H', k)[0], byte_vals[k])

if __name__ == '__main__':
    main()
