import sys
from cStringIO import StringIO

if __name__ == '__main__':
  with open(sys.argv[1], 'rb') as f:
    data = f.read()

  out = StringIO()
  out.write('def execve_shellcode(cmd):\n\n'
            '  shellcode = bytearray(\n')

  done = False
  idx = 0

  while not done:
    byte_str = []
    while idx < len(data):
      byte_str.append('\\x%02x' % (ord(data[idx])))
      idx += 1

      if idx % 16 == 0:
        break

    out.write('    \'%s\'\n' % ''.join(byte_str))


    if idx >= len(data):
      done = True

  out.write('    +  cmd + \'\\x00\')\n'
            '\n'
            '  return shellcode')

  print out.getvalue()
