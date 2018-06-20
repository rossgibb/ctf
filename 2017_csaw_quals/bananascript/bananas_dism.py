import itertools
import subprocess
import os
import fcntl
import sys

def all_bananas():

    b1 = ['b', 'B']
    b2 = ['a', 'A']
    b3 = ['n', 'N']
    b4 = ['a', 'A']
    b5 = ['n', 'N']
    b6 = ['a', 'A']
    b7 = ['s', 'S']

    for a in itertools.product(b1, b2, b3, b4, b5, b6, b7):
        yield ''.join(a)

def idx_to_bananas(idx):

    ret_val = ''

    if idx & 0x40:
        ret_val += 'b'
    else:
        ret_val += 'B'
    if idx & 0x20:
        ret_val += 'a'
    else:
        ret_val += 'A'
    if idx & 0x10:
        ret_val += 'n'
    else:
        ret_val += 'N'
    if idx & 0x08:
        ret_val += 'a'
    else:
        ret_val += 'A'
    if idx & 0x04:
        ret_val += 'n'
    else:
        ret_val += 'N'
    if idx & 0x02:
        ret_val += 'a'
    else:
        ret_val += 'A'
    if idx & 0x01:
        ret_val += 's'
    else:
        ret_val += 'S'

    return ret_val

def build_alphabet():
    bananas_to_char = {}

    idx = 0

    for code in range(ord('a'), ord('z') + 1):
        bananas_to_char[idx_to_bananas(idx)] = chr(code)
        idx += 1

    for code in range(ord('A'), ord('Z') + 1):
        bananas_to_char[idx_to_bananas(idx)] = chr(code)
        idx += 1

    bananas_to_char[idx_to_bananas(idx)] = ' '
    idx += 2

    for code in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',',
                 '.', '/', ';', "'", '[', ']', '=', '-', '`', '~', '!', '@',
                 '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}',
                 '\\',':', '"', '?', '>', '<']:
        bananas_to_char[idx_to_bananas(idx)] = code
        idx += 1 

    char_to_bananas = {}

    for banana in bananas_to_char:
        char_to_bananas[bananas_to_char[banana]] = banana

    return bananas_to_char, char_to_bananas

bananas_to_char = None
char_to_bananas = None
def get_banana_mappings():
    global bananas_to_char, char_to_bananas

    if bananas_to_char is None or char_to_bananas is None:
        bananas_to_char, char_to_bananas = build_alphabet()

    return bananas_to_char, char_to_bananas

def banana_to_char(banana):

    bananas_to_char, char_to_bananas = get_banana_mappings()

    return bananas_to_char[banana] if banana in bananas_to_char else '?'

def decode(encoded, key):
    encoded_idx = len(encoded) - 1
    key_idx = len(key) - 1
    token_idx = 0
    decoded = ''

    while encoded_idx >= 0:
        if encoded[encoded_idx] == ' ':
            encoded_idx -= 1
            token_idx = 0
            decoded = ' ' + decoded
            key_idx
            continue

        key_idx = len(key) - (len(decoded) % (len(key) + 1)) - 1

        if encoded[encoded_idx] == key[key_idx]:
            if token_idx == 0:
                decoded = 's' + decoded
            elif token_idx == 1 or token_idx == 3 or token_idx == 5:
                decoded = 'a' + decoded
            elif token_idx == 2 or token_idx == 4:
                decoded = 'n' + decoded
            elif token_idx == 6:
                decoded = 'b' + decoded
        else:
            if token_idx == 0:
                decoded = 'S' + decoded
            elif token_idx == 1 or token_idx == 3 or token_idx == 5:
                decoded = 'A' + decoded
            elif token_idx == 2 or token_idx == 4:
                decoded = 'N' + decoded
            elif token_idx == 6:
                decoded = 'B' + decoded
        token_idx += 1
        encoded_idx -= 1

    return decoded

def bananas_to_str(bananas):
    bananas_to_char, _ = get_banana_mappings()

    ret_val = ''

    for banana in bananas.split(' '):
        if banana not in bananas_to_char:
            return None
        else:
            ret_val += banana_to_char(banana)

    return ret_val

def str_to_bananas(in_str):
    _, char_to_bananas = get_banana_mappings()

    ret_val = []

    for c in in_str:
        ret_val.append(char_to_bananas[c])

    return ' '.join(ret_val)

def execute_line(tokens, state):
    operand = {'banANAS':1, 'banANAs':2, 'banANaS':3, 'banANas':4,
               'banAnAS':5, 'banAnAs':6, 'banAnaS':7, 'banAnas':8}


    if tokens[0] in operand:
        if not tokens[2].startswith('banA'):
            if tokens[1] == 'baNanas':
                key = 'str_reg_%s' % (operand[tokens[0]])
                state[key] = ' '.join(tokens[2:])
                value = bananas_to_str(state[key])
                ret_str = '# push str from index 2 %s' % (key)
                if value is not None:
                    ret_str += '\n# %s' % (value)
                return ret_str, state
            else:
                return '# Comment: %s' % (''.join(banana_to_char(x) for x in tokens[2:])), state
        else:
            if tokens[1] == 'baNanAS':
                encoded_k = 'str_reg_%s' % (operand[tokens[0]])
                key_k = 'str_reg_%s' % (operand[tokens[2]])
                state['reg_1'] = decode(state[encoded_k], state[key_k])
                plain_text = ''.join([banana_to_char(x) for x in state['reg_1'].split(' ')])
                print '%s\n' % (plain_text)
                return '# decode %s:encoded %s:key into reg_1\n# %s' % (encoded_k, key_k, plain_text), state
            elif tokens[1] == 'baNAnas':
                encoded_k = 'str_reg_%s' % (operand[tokens[0]])
                key_k = 'str_reg_%s' % (operand[tokens[2]])
                #state['reg_1'] = decode(state[encoded_k], state[key_k])
                #print state['reg_1']
                #plain_text = ''.join([banana_to_char(x) for x in state['reg_1'].split(' ')])
                return '# decode %s:encoded %s:key into reg_1' % (encoded_k, key_k), state

    if tokens[0] == 'bananas':
        return '# print output str_reg_%s' % (operand[tokens[1]]), state
    elif tokens[0] == 'bananaS':
        key = 'str_reg_%s' % (operand[tokens[1]])
        data = raw_input("Input: ")
        state[key] = data
        return '# set input to %s and read line of input there' % (key), state
    elif tokens[0] == 'bananAS':
        if tokens[1] in operand:
            if tokens[2] == 'baNanas':
                key = 'int_reg_%s' % (operand[tokens[1]])
                state[key] = ' '.join(tokens[3:])
                value = ''.join([banana_to_char(x) for x in state[key].split(' ')])
                return '# push int from index 3 %s\n%s' % (key, value), state
    elif tokens[0] == 'banaNAS':
        if tokens[1] in operand and tokens[3] in operand:
            if tokens[2] ==  'baNANaS':
                op1 = 'str_reg_%s' % (operand[tokens[1]])
                op2 = 'str_reg_%s' % (operand[tokens[3]])
                return '# compare_1 %s with %s' % (op1, op2), state
            elif tokens[2] == 'baNANAS':
                op1 = 'str_reg_%s' % (operand[tokens[1]])
                op2 = 'str_reg_%s' % (operand[tokens[3]])
                return '# compare_2 %s with %s' % (op1, op2), state
    elif tokens[0] == 'bananAs':
        if tokens[1] == 'bananAS':
            op1 = 'int_reg_%s' % (operand[tokens[2]])
            return '# jump value in %s (%s)' % (op1, ''.join([banana_to_char(x) for x in state[op1].split(' ')])), state

    return '# Unknown', state

if __name__ == '__main__':

    state = {'str_reg_1': '',
             'str_reg_2': '',
             'str_reg_3': '',
             'str_reg_4': '',
             'str_reg_5': '',
             'str_reg_6': '',
             'str_reg_7': '',
             'str_reg_8': '',
             'str_int_1': '',
             'str_int_2': '',
             'str_int_3': '',
             'str_int_4': '',
             'str_int_5': '',
             'str_int_6': '',
             'str_int_7': '',
             'str_int_8': '',
             'reg_1': '',
             'reg_2': '',
             'reg_3': '',
             'reg_4': ''}

    with open(sys.argv[1], 'rb') as f, open('%s.dism' % (sys.argv[1]), 'wb') as o:
        for line in f:
            words = line.strip().split(' ')

            dism, state = execute_line(words, state)
            o.write('%s\n' % (dism))
            o.write('%s\n\n' % (' '.join(words)))
