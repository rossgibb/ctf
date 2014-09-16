import sys
import string
from collections import defaultdict

def usage():
    print '%s file [substituion]' % (sys.argv[0])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        quit()

    with open(sys.argv[1], 'rb') as f:
        data = f.read().strip()

    letters = defaultdict(int)

    total = 0

    for c in data:
        if c in string.ascii_uppercase or c in string.ascii_lowercase:
            letters[c] += 1
            total += 1

    frequency_dict = {}
    frequency_str = ''

    print 'Frequency analysis:'

    for i, k in enumerate(sorted(letters, key=letters.get, reverse=True)):
        frequency_dict[k] = i
        frequency_str += k
        print '%s: %s (%0.4f%%)' % (k, letters[k], letters[k] / float(total) * 100)

    if len(sys.argv) > 2:
        substitution = sys.argv[2]
    else:
        # Based on analysis of English text
        substitution = 'etaoinshrdlcumwfgypbvkjxqz'

    print '\nTo try again enter the following, but reorder the substitution string.'
    print '\n%s %s %s' % (sys.argv[0], sys.argv[1], substitution)

    substitution_dict = {}

    for i, c in enumerate(substitution):
        substitution_dict[i] = c


    print '\nDecrypted Text:\n'

    for c in data:
        if c in frequency_dict:
            sys.stdout.write(substitution_dict[frequency_dict[c]])
        else:
            sys.stdout.write(c)

    print '\n'
