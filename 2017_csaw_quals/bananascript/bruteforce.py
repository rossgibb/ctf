import bananas_dism
from itertools import product
from itertools import permutations
import re

# Produces all possible bananas
def all_bananas():

    b1 = ['b', 'B']
    b2 = ['a', 'A']
    b3 = ['n', 'N']
    b4 = ['a', 'A']
    b5 = ['n', 'N']
    b6 = ['a', 'A']
    b7 = ['s', 'S']

    for a in product(b1, b2, b3, b4, b5, b6, b7):
        yield ''.join(a)

encoded = 'baNANAs banAnAS banANaS banaNAs BANANAs BANaNas BANAnas bANanAS baNaNAs banaNAs bANaNas BaNaNaS baNanas BaNaNas BaNanas BaNANas baNAnaS banaNAS bANAnAs banANAS bAnaNAs BANAnAS BANAnas BaNANas bAnANas BaNaNaS banAnAs bANAnAs baNaNas BanaNaS bANANas banaNas bAnANaS bANANaS BaNAnas baNanAs baNanAS BaNAnAs bANANas banAnas bAnanaS banANaS bANaNAS banANaS baNanAS BaNanAS BANAnAS BaNanaS'

encoded_l = encoded.split(' ')

# assume the flag starts with flag{
key_begin = [bananas_dism.decode(encoded_l[0], bananas_dism.str_to_bananas('f')),
             bananas_dism.decode(encoded_l[1], bananas_dism.str_to_bananas('l')),
             bananas_dism.decode(encoded_l[2], bananas_dism.str_to_bananas('a')),
             bananas_dism.decode(encoded_l[3], bananas_dism.str_to_bananas('g')),
             bananas_dism.decode(encoded_l[4], bananas_dism.str_to_bananas('{'))]

# assume the flag ends with }
key_end = [bananas_dism.decode(encoded_l[len(encoded_l) - 1], bananas_dism.str_to_bananas('}'))]

results = set()

for needle in permutations([x for x in all_bananas()] + [x for x in all_bananas()], r=2):
    key = ' '.join(key_begin + list(needle) + key_end)
    result = bananas_dism.decode(encoded, key)
    result = bananas_dism.bananas_to_str(result)
    # Need to filter out keys that are not 31337 speak, some trial and error finding this
    if result is not None and re.search(r'^flag\{[0-9A-Za-z_]+\}$', result):
        results.add(result)

for result in sorted(results):
    print result
