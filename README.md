# PMNG-Cipher
Polymapping N-gram cipher.

## Algorithm
The cipher is a substituion cipher with three additions. The first is that some plaintext characters encrypt to the same ciphertext character. As a result, when decrypting, some characters have two possible plaintext counterparts. These are indicated in bold and italics in the table below.

Plaintext | Ciphertext
------ | ------
A | O
B | V
_**C**_ | _**K**_
D | g
E | Y
_**F**_ | _**F**_
_**G**_ | _**Q**_
H | J
I | L
J | Q
K | K
L | M
N | T
O | W
P | B
_**Q**_ | _**Z**_
R | A
S | C
T | P
_**U**_ | _**X**_
_**V**_ | _**X**_
W | N
_**X**_ | _**Z**_
Y | H
_**Z**_ | _**Z**_

Additionally, certain N-grams in plaintext are encrypted into single characters. For clarity, these N-gram mappings and polymapped characters are summarised below.

Plaintext | Ciphertext
------ | ------
ING | I
ST | S
EA | E
OU | U
TH | F
`-----` | `-----`
F, TH | F
C, K | K
G, J | Q
U, V | X
Q, X, Z | Z

Finally, double letters are encrypted differently. In ciphertext, a double letter is notated by a `D` followed by the letter that is doubled. For example, the plaintext word `BELL` would encrypt to `VYDM`. The `BE` encrypts to `VY`, and `L` maps to `M`. Because `M` is prefaced with a `D`, it would expand to `VYMM` which then decrypts back to `BELL`.
