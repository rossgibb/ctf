## Challenge description

```
Not too sure how to Interpret this, the lab member who wrote this "forgot" to write any documentation. This s***, and him, is bananas. B, A-N-A-N-A-S.
```

## Analysis

As usual the problem description is vague, but does allude to an __interpreter__ and __bananas__.

We are given two files. A 64-bit ELF executable [moneyDo](monkeyDo) and text file called [banana.script](banana.script), which is entirely filled with the word `bananas` in various capitalizations.

Running the program with the script as an argument runs a program where the user interacts with a group of grumpy monkies.

```
$ ./monkeyDo banana.script 
Hello! And welcome to the Flying Monkeys' Fantastic Falling Fan Trivia Game.
 
Here, the council of monkeys will ask you questions, which will determine whether they choose to lift you away save you from your plummeting fate.
 
"WRITE DOWN YOUR AGE," speaks the elder monkey.

...

22
 
~How can monkeys talk? And why am I following you their commands?~
 
"WRITE DOWN YOUR SSN/CVV's/privatekeys- err I mean favourite food!," speaks the elder monkey.
bananas
 
"GASP!" All the monkeys are dreadfully appaled, some of them even start to cry.  "How could you?" spits one monkey, covering the eyes of their child.  The conglomerate of monkeys take off from the platform, leaving you to fall to your death.
```

It seems we have to answer the questions correctly to get the flag

It also seems that `monkeyDo` interprets a scripting language made up entirely of the string `bananas`

This hypothesis can be verified by running `strings` on the `monkeyDo` binary which reveals a large number of `bananas` strings in various capitalizations.

## Reverse engineering

Opening up the binary and navigating to the `main` function reveals a very large and complicated function, that does appear to interpret a `bananas` based script.

Before attempting to reverse engineer `main`, it was noticed that not all the references to the `bananas` strings are within `main`, many are also are referenced in the functions at `0x4020f6` and `0x405d09`. Looking at these two functions reveals a mapping between the `bananas` strings in various capitalizations and ascii characters.

Theis mapping can be demonsrated with the following python functions.
```python
>>> str_to_bananas('hello world')
'BANAnas BANAnAS BANaNas BANaNas BANanaS BanAnAS BAnAnaS BANanaS BAnANAs BANaNas BANANas'
>>> bananas_to_str('BANAnas BANAnAS BANaNas BANaNas BANanaS BanAnAS BAnAnaS BANanaS BAnANAs BANaNas BANANas')
'hello world'
```

A naive solution is to simply convert all the `bananas` in `banana.script` to ascii. While this does reveal some readable English text, it doesn't reveal the answers to the questions asked by the monkeys nor does it reveal the flag.

To solve this challenge we will most likely have to disassemble `banana.script`.

In general, a programming langage usually has the form:
```
cmd_verb operand_1 operand_2 operand_3 ...
```

Using a debugger and IDA Pro the `main` function can slowly be stepped through and the format of each command can be understood.

The script [bananas_dism.py](bananas_dism.py) implements a [banana.script](banana.script) disassembler and emulator.

```bash
$ python bananas_dism.py banana.script
```

This produces the the file [banana.scirpt.dism](banana.script.dism) that adds a comment to each command with its disassembled equivalent.

The disassembly reveals the answer to the question, "What is your favourite food?" The answer being: `BanaNAs!`. However, the rest of the answers are not revealed in the disassembly.

What is clear from the disassembly is that the flag is decoded using the following logic:
```
flag = decode(encoded_flag, decode(decode(decode(favourite_food, age), name), favourite_colour))
```

Since we only know the correct value of `favourite_food` we are left with trying guess the other values. This would likely be difficult, since at each stage we would not really know if we had a correct value for each stage.

At this point we need to take avantage of the fact we do know that the plain text flag will begin with `flag{` and end with `}`. We also know that the length of `favourite_food` is 8 characters, so each stage of the decode will also be 8 characters.

Using this knowlede we can create a bruteforce decoding script, [bruteforce.py](bruteforce.py).

```bash
$  python bruteforce.py
flag{0r4ng3_3w3_ch1pp3r_1_h47h_n07_s4y_b4n4n4rs}
flag{1r4ng3_3x3_ch1pp2r_1_h47g_n07_s4z_b4n4n4qs}
flag{2r4ng3_3y3_ch1pp1r_1_h47j_n07_s4w_b4n4n4Fs}
flag{3r4ng3_3z3_ch1pp0r_1_h47i_n07_s4x_b4n4n4Es}
flag{6r4ng3_3C3_ch1ppZr_1_h47n_n07_s4s_b4n4n4Bs}
flag{7r4ng3_3D3_ch1ppYr_1_h47m_n07_s4t_b4n4n4As}
flag{8r4ng3_3E3_ch1ppXr_1_h47p_n07_s4q_b4n4n4zs}
flag{9r4ng3_3F3_ch1ppWr_1_h47o_n07_s4r_b4n4n4ys}
flag{Cr4ng3_363_ch1pptr_1_h47T_n07_s4Y_b4n4n45s}
flag{Dr4ng3_373_ch1ppsr_1_h47S_n07_s4Z_b4n4n44s}
...
```

The bruteforce scirpt products quite a few candidates, some are filtered out if they don't contain characters that create a `1337` string. A total of about 56 candidate strings are produced.

Reviewing strings manually shows that the first candidate is likely the flag:
```
flag{0r4ng3_3w3_ch1pp3r_1_h47h_n07_s4y_b4n4n4rs}
```

Which translates to `Orange ewe chipper I hath not say bananars`
