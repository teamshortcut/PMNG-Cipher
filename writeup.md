# Challenge
## Ciphertext
`SOAP2 NLF3 FLC1 TXRVYA0 GUVMY4 LP1 OTG3 ODG1 FLC0 AY-KOMKXMOPY4 OC2 O1 VEAI2 OTG1 ODG3 FLC0 FLTODMH1 GLXLGY6 VH9 FLC0`

## Briefing
### Cryptically Coded Ingenious Instructions

We've intercepted a cipher, which you'll find in cipher.txt. We believe it contains some kind of instructions. Crack the cipher, follow the instructions, get the flag! Easy...

By teamshortcut

## Hints
The challenge had 3 successive hints.

1. The numbers are not meaningless, but it will be easier to strip them out and set them aside for later; focus on just the letters.
2. The cipher is solvable using medieval-era techniques, and is designed to trip up most automated cipher solving sites/tools.
3. The (working) title of the cipher is a Polymapping N-gram Substitution cipher, though that omits one final quirk to be solved.

## Walkthrough

There are several ways to approach this challenge, but one possible walkthrough is outlined here. The full algorithm for this cipher is detailed in [README.md](README.md).

First, notice that the text is already spaced as if natural language. For now, it is easier to ignore the numbers. You can work this out by seeing the differing numbers on the end of `FLC`, by seeing that intuitive solutions using the numbers (a ROT shift for example) do not yield any results, or from the first hint.

The next step is to check the entropy of the text, or perform a frequency analysis of the text. This shows that the text _appears_ to be regular English text, put through a monoalphabetic cipher. (this is half right!)

A logical next step is to run the text through automated online substitution cipher solvers, which will fail to return any meaningful text, indicating that the cipher is more complex. The easiest place to start is to look at the word `AY-KOMKXMOPY` as it is hyphenated.

As the word is hyphenated, we can deduce some likely two-letter prefixes in English. Looking at the length of the word and pattern of the letters in it, you can deduce/enumerate potential candidates. This can be done manually (the whole challenge is doable with just a pen and paper!), with a script, or even online tools like a crossword solver! Using this information, we can deduce that this word is probably `re-calculate`.

Going off this assumption, we can fill in some of the rest of the ciphertext. Using a similar approach and combining the techniques and knowledge from before, we can try and deduce other letters and/or words. At this point though, it will become clear that this alphabet cannot be entirely consistent with proper English words. It's not possible to form proper English words with a typical mono-alphabetic approach, but a lot of words can be approximated.

At this point, you can take different approaches, but it should be clear that there are some additional layers to the cipher than a normal mono-alphabetic substitution. One thing to note is that there are no double letters in the ciphertext. From context (and a lot of experimentation and persistence), you can realise that double letters are encrypted with a `D` to double the letter in front of it. For example, you might reach `finaDly` and realise that `D` must double the `l` in front to transform the word into `finally`. After this, you might discover one of the remaining "twists", that certain letters are polymapped; that is, that a ciphertext character can decrypt to multiple characters. This may become clear, for example, after using letters from `re-calculate` and other words from context to reach `diuide`, where `X` had decrypted to `u` in `re-calculate`. Clearly, this word is `divide`, so `X` can decrypt to both `u` and `v`. These characters are grouped together linguistically, as are the other polymapped characters. Finally, certain characters decrypt to n-grams. (common grouping of characters, like `th` or `ou`) This may become clear from a few points, but among them `number[,] dUble it`. From context, `dUble` can be deduced to be `double`, which means that `U` decrypts to `ou`. Again, this is linguistically linked. The cipher is detailed fully in [src/README.md](src/README.md). By deducing these extra layers, it's possible to work through the cipher and produce the plaintext.

Once we have the plaintext, we need to re-add the numbers after each word.
```
Start2 with3 this1 number0
Double4 it1 and3 add1 this0
Re-calculate4 as2 a1 bearing2 and1 add3 this0
Finally1 divide6 by9 this0
```
Splitting the instructions into steps like this, it becomes clear that `0` appears at the end of each line and nowhere else. The plaintext is a set of mathematical instructions, that operate on numbers formed from the digits after each word, where `0` acts a delimiter.
This gives the numbers 231, 4131, 421213, and 169. Following the instructions with these numbers gives us the flag!

```
(231 * 2) + 4131 = 4593
(4593 mod 360) + 421213 = 273 + 421213 = 421486
421486 / 169 = 2494
```
