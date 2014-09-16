# Description

On the back of the broken panel you see a recovery [manual](read_the_manual.txt). You need to find the emergency repair key in order to put the robot into autoboot mode, but it appears to be ciphered using a Caesar cipher.

## Solution

A caesar cipher works by shifting letters by a constant ammount. For example, if all chacters are shifted right two, then the alphabet 'abcde...' becomes 'yzabc...' (the end of the alphabet wraps around to the front).

The challenge gives us a file enrypted with a caesar cipher with an unknown shift. Looking at the file it appears that punctuation and whitespace are not shifted, only letters are shifted. It also appears that the case of a letter is preserved.

We have two choices we can assume the orginal plain text is English and do character frequency analysis, this analysis will likely give the shift used and the decryption can then be done using that shift. Alternatively, we we can simply decrypt the text using all possible caesar shifts (there are only 25) and examine each decrypted text looking for English text. Either way we probably want to a script that can perform caesar shift on a file with an arbitrary shift..

The input for the script will be a file containing the cipher text, a file to write the output to, and shift ammount to use.

<pre>
caesar_derypt.py INPUT_FILE OUTPUT_FILE [SHIFT]

Reads in INPUT_FILE does a caesar cipher decryption and outputs
it to OUTPUT_FILE. You can optionally specify ammount of right shift to use.
.i.e. a shift of 2 results in the alphabet 'abcde...' shifted to 'yzabc...',
default shift is 13.
</pre>

Once we have a general caesar decryption script and since there are only 25 possible shifts of the alphabet, we can easily generate all possible decryptions of the cipher text. Once we have all the decription we can look for common English words that are likely to appear and that should give us the plain text.

Create all the cipher texts using a bash for loop:
<pre>
for i in {1..25}; do python caesar_decrypt.py read_the_manual.txt out_${i}.txt $i; done
</pre>

This will give 25 files. We then search inside them for the common English word "the", the file with the highest frequency of the word "the" is likely English text.

<pre>
$ grep -c "the" out_*.txt
out_10.txt:0
out_11.txt:0
out_12.txt:0
out_13.txt:0
out_14.txt:2
out_15.txt:0
out_16.txt:11
out_17.txt:0
out_18.txt:0
out_19.txt:0
out_1.txt:0
out_20.txt:0
out_21.txt:0
out_22.txt:0
out_23.txt:0
out_24.txt:0
out_25.txt:0
out_2.txt:0
out_3.txt:27
out_4.txt:0
out_5.txt:0
out_6.txt:0
out_7.txt:0
out_8.txt:0
out_9.txt:0
</pre>

Sure enough, out_3.txt contains what we're after.
