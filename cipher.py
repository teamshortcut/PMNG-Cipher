# Poly-mapping N-gram cipher

import sys
from wordfreq import word_frequency

# TODO: handle splitting numbers, if numbers are contained within words,
# if words are not split by space (maybe split by number, maybe nothing)

# D means double the next character

HELP_MESSAGE = """Usage:
cipher.py [-h] [-d] text
-h : displays this help message
-d : decrypts the given text (default is encrypt)
"""
# normal substitution mappings

# plaintext to ciphertext (single 1:1 mappings)
encrypt_mapping = {"A": "O",
                   "B": "V",
                   "D": "G",
                   "E": "Y",
                   "H": "J",
                   "I": "L",
                   "L": "M",
                   "M": "R",
                   "N": "T",
                   "O": "W",
                   "P": "B",
                   "R": "A",
                   "S": "C",
                   "T": "P",
                   "W": "N",
                   "Y": "H",
                  }
decrypt_mapping = {v: k for k, v in encrypt_mapping.items()} # ciphertext to plaintext

encrypt_polymappings = {"C": "k",
						"F": "f",
						"G": "q",
						"J": "q",
						"K": "k",
						"Q": "z",
						"U": "x",
						"V": "x",
						"X": "z",
						"Z": "z",
						}
decrypt_polymappings = {"F": ["f", "th"],
						"K": ["c", "k"],
						"Q": ["g", "j"],
						"X": ["u", "v"],
						"Z": ["q", "x", "z"]
						}

encrypt_polygrams = {"TH": "f",
					 "OU": "u",
					 "EA": "e",
					 "ING": "i",
					 "ST": "s"
					}
decrypt_polygrams = {v.upper(): k.lower() for k, v in encrypt_polygrams.items()}
del decrypt_polygrams["F"] # should only be decrypted in polymappings, as could decrypt to F or TH

def tryForMappedCharEncrypt(char):
	if char in encrypt_mapping.keys():
		return encrypt_mapping[char]
	elif char in encrypt_polygrams.keys():
		return encrypt_polygrams[char]
	elif char in encrypt_polymappings.keys():
		return encrypt_polymappings[char]
	else:
		return char

def tryForMappedCharDecrypt(char):
	if char in decrypt_mapping.keys():
		return decrypt_mapping[char].lower()
	elif char in decrypt_polygrams.keys():
		return decrypt_polygrams[char].lower()
	else:
		return char

def getPolymappingPossibilities(ciphertext, possibilities, cipher_chars):
	i = 0
	if ciphertext.islower():
		possibilities.append(ciphertext)
		return possibilities

	while i < len(ciphertext):
		char = ciphertext[i]
		if char in cipher_chars:
			local_possibilities = []
			for c in decrypt_polymappings[char]:
				local_possibilities.append(ciphertext[:i] + c + ciphertext[i+1:])
			
			for p in local_possibilities:
				possibilities = getPolymappingPossibilities(p, possibilities, cipher_chars)

		i += 1

	return list(set(possibilities))

def word_freq(word):
	return word_frequency(word, "en")

def decryptPolymapings(ciphertext):
	plaintext = []

	for word in ciphertext.split():
		cipher_chars = []

		for cipher_char in decrypt_polymappings.keys():
			if cipher_char in word:
				cipher_chars.append(cipher_char)

		# substitutions to make
		if cipher_chars:
			possibilities = getPolymappingPossibilities(word, [], cipher_chars)
			possibilities = sorted(possibilities, key=word_freq)
			plaintext.append(possibilities[-1])
		else:
			plaintext.append(word)

	return " ".join(plaintext)

def decrypt(ciphertext, separateNumbers):
	ciphertext = ciphertext.upper()
	plaintext = ""
	numbers = []

	index = 0
	while index < len(ciphertext):
		char = ciphertext[index]
		if char == "D":
			plainChar = tryForMappedCharDecrypt(ciphertext[index+1])
			if plainChar not in decrypt_polymappings.keys():
				plainChar = plainChar.lower()

			plaintext += plainChar*2
			index += 1
		else:
			if not(separateNumbers and char.isdigit()):
				plaintext += tryForMappedCharDecrypt(char)
			else:
				numbers.append(char)
		index += 1

	plaintext = decryptPolymapings(plaintext)
	return plaintext + "\n" + "".join(numbers)


def encryptDoubleChars(plaintext):
	index = 0
	while index < len(plaintext) - 1:
		if plaintext[index] == plaintext[index+1]:
			plaintext = plaintext[:index] + "D" + plaintext[index+1:]
			index += 1
		index += 1

	return plaintext

def encrypt(plaintext):
	plaintext = plaintext.upper()
	ciphertext = plaintext

	alphabet = list(encrypt_polygrams.keys()) + list(encrypt_polymappings.keys()) + list(encrypt_mapping.keys())

	for char in alphabet:
		ciphertext = ciphertext.replace(char, tryForMappedCharEncrypt(char).lower())

	ciphertext = ciphertext.upper()

	return encryptDoubleChars(ciphertext)

if __name__ == "__main__":
	stdinput = not sys.stdin.isatty()
	if len(sys.argv) <= 1 and not stdinput:
		print("At least one argument must be provided.")
	elif len(sys.argv) > 1 and sys.argv[1] == "-h":
		print(HELP_MESSAGE)
	elif len(sys.argv) > 1 and sys.argv[1] == "-d":
		if len(sys.argv) < 3 and not stdinput:
			print("Please provide ciphertext to decrypt.")
		else:
			if stdinput:
				code = sys.stdin.read()
			else:
				code = sys.argv[2]
			print(decrypt(code, True))
	else:
		if stdinput:
			code = sys.stdin.read()
		else:
			code = sys.argv[1]
		print(encrypt(code))
