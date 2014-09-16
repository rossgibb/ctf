# Challenge
Someone or something stuck a random flyer on your space ship that reads:

<pre>
cslcehesehft ohrumvc zmvm scmk ht ptohmte ehbmc mxmt eufsju eumq pvm dshem mpchgq lvfymt zheu nsce p rmtohg ptk rprmv, fv bfvm vmomtegq lq ofbbft ofbrsemvhwmk effgc. qfsv ymq hc: zumt_kf_zm_jme_ef_eum_upvk_cesii
</pre>

## Solution

There isn't a specific clue given for this puzzle, so all we have is the challenge text to go on.

Since the challenge mentions 'random' and the cipher text appears to match english text with scrambled letters (notice the word spacing and puncuation) a good first guess is a [substitution cipher] (http://en.wikipedia.org/wiki/Substitution_cipher).

A substitution cipher is made by mixing up the english letters in any order, but doing so consistently. So if 'a' becomes 'u', and 'b' becomes 'r', and so on, that mapping must remain constant.

If we know what language our target plain text is in we can do a character frequency analysis on the cipher text to recover the plain text. For instance, in English certain characters, like vowels, appear much more often than characters like 'x' or 'z'.

A script can help us with the analysis. The script is used as follows:

<pre>
frequency_analysis.py file [substituion]
</pre>

The script takes a file with text we are trying to decrypt and a substituion string for how to substitute the letters.

The default substituion string is: etoinrsuhacymdplwbfgkqjzvx

Meaning, that 'e' is the most frequent character in expected, followed by 't', and so on. This default the actual frequency of letters sampled over a very large set of English text.

After being run once using the default character frequency substitution the following text is displayed:

<pre>
Decrypted Text:

shystothtoai lowrens gene hsem oi diloeit toues eqei trahbr trec dne khote edsofc ynavei gotr jhst d weilof dim wdwen, an uane neleitfc yc lauuai lauwhtenoxem taafs. cahn vec os: grei_ma_ge_bet_ta_tre_rdnm_sthpp
</pre>

The text is certainly not decrypted, but looking closely you can see some likely English words. The first word in particular is very close to 'substitution'. By slowly reordering the second command line argument from the default substituion string the entire plain text can be recovered. 
