import sys

def usage():
    print '\n%s <input_file> <output_file> [shift]\n' % (sys.argv[0])
    print ('Reads in <input_file> does a caesar cipher decryption and outputs\n'
           'it to <output_file>. You can optionally specify ammount of right shift to use.\n.'
           'i.e. a shift of 2 results in \'yzabc...\', default shift is 13.' )

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
        quit()

    in_f = sys.argv[1]
    out_f = sys.argv[2]

    if len(sys.argv) > 3:
        shift = int(sys.argv[3])
    else:
        shift = 13

    replace_table = {}

    # Create replacement table
    for i, letter in enumerate('abcdefghijklmnopqrstuvwxyz'):
        replace_table[i] = chr(((i - shift) % 26) + ord('a'))

    with open(in_f, 'rb') as f:
        with open(out_f, 'wb') as o:
            chunk = f.read(1024)

            while chunk != '':
                out = []
                for c in chunk:
                    if ord(c) >= ord('a') and ord(c) <= ord('z'):
                        out.append(replace_table[ord(c) - ord('a')])
                    elif ord(c) >= ord('A') and ord(c) <= ord('Z'):
                        out.append(replace_table[ord(c) - ord('A')].upper())
                    else:
                        out.append(c)

                o.write(''.join(out))
                chunk = f.read(1024)
