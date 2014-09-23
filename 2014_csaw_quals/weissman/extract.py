import sys
import struct
import os

def main():
    with open(sys.argv[1], 'rb') as f:
        data = f.read()

    magic, version, num_files = struct.unpack('<8sII', data[:0x10])

    cur_idx = 0x10
    file_idx = 0

    for i in range(num_files):
        magic, comp_sz, ucomp_sz, filename = struct.unpack('<III32s', data[cur_idx:cur_idx + (0x4 * 3) + 0x20])

        if i > 0: print ''
        print 'File: %s' % (filename)
        print 'magic: %x' % (magic)
        print 'Compressed size: %s' % (comp_sz)
        print 'Uncompressed size: %s' % (ucomp_sz)

        cur_idx += 0x2c

        file_data = data[cur_idx:cur_idx + comp_sz]

        with open('%s_file_%s.bin' % (os.path.splitext(sys.argv[1])[0], file_idx), 'wb') as o:
            o.write(file_data)

        cur_idx += comp_sz
        file_idx += 1

if __name__ == '__main__':
    main()
