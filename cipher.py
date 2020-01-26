# Poly-mapping N-gram cipher

import re
import sys
from wordfreq import word_frequency

HELP_MESSAGE = """Usage:
cipher.py [-h] [-d] text
-h : displays this help message
-d : decrypts the given text (default is encrypt)
-n : separates numbers
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

# multiple plaintext characters map to the same ciphertext character
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

# certain n-grams (common groups of characters) encrypt to single ciphertext characters
encrypt_ngrams = {"TH": "f",
				  "OU": "u",
				  "EA": "e",
				  "ING": "i",
				  "ST": "s"
				 }
# uppercase for unprocessed, lowercase for characters that have been replaced
decrypt_ngrams = {v.upper(): k.lower() for k, v in encrypt_ngrams.items()}
del decrypt_ngrams["F"] # should only be decrypted in polymappings, as could decrypt to F or TH

# returns the encrypted equivalent of a plaintext character, if it exists in any mapping
def tryForMappedCharEncrypt(char):
	if char in encrypt_mapping.keys():
		return encrypt_mapping[char]
	elif char in encrypt_ngrams.keys():
		return encrypt_ngrams[char]
	elif char in encrypt_polymappings.keys():
		return encrypt_polymappings[char]
	else:
		return char

# returns the decrypted equivalent of a ciphertext character, if it exists in standard/n-gram mapping
# does not check for polymappings, this is handled separately
def tryForMappedCharDecrypt(char):
	if char in decrypt_mapping.keys():
		return decrypt_mapping[char].lower()
	elif char in decrypt_ngrams.keys():
		return decrypt_ngrams[char].lower()
	else:
		return char

# recursive function to get all the combinations of possible decryptions with polymappings
# expects a partially decrypted ciphertext, the current possibilities (pass [] to start) and the characters to check mappings for
def getPolymappingPossibilities(ciphertext, possibilities, cipher_chars):
	if ciphertext.islower(): # fully decrypted
		possibilities.append(ciphertext)
		return possibilities

	i = 0
	while i < len(ciphertext):
		char = ciphertext[i]
		if char in cipher_chars:
			local_possibilities = []
			for c in decrypt_polymappings[char]: # all possibilities for decrypting this character
				local_possibilities.append(ciphertext[:i] + c + ciphertext[i+1:])
			
			for p in local_possibilities:
				# all combinations of further characters
				possibilities = getPolymappingPossibilities(p, possibilities, cipher_chars)

		i += 1

	return list(set(possibilities)) # unique results

def word_freq(word):
	return word_frequency(word, "en")

# decrypts the polymappings of a partially decrypted ciphertext
def decryptPolymapings(ciphertext):
	plaintext = []

	for word in ciphertext.split():
		cipher_chars = []

		for cipher_char in decrypt_polymappings.keys():
			if cipher_char in word:
				cipher_chars.append(cipher_char)

		# substitutions to make
		if cipher_chars:
			# all possible decryptions based on all combinations of polymappings
			possibilities = getPolymappingPossibilities(word, [], cipher_chars)
			possibilities = sorted(possibilities, key=word_freq) # find the closest to english based on the frequency of the word
			plaintext.append(possibilities[-1]) # last item is most frequent
		else:
			plaintext.append(word)

	return " ".join(plaintext)

def decrypt(ciphertext, separateNumbers):
	ciphertext = ciphertext.upper()
	plaintext = ""
	numbers = []

	# if the text isn't split by words, split it up by numbers
	if " " not in ciphertext and any(char.isdigit() for char in ciphertext):
		ciphertext = " ".join(re.split("(0|1|2|3|4|5|6|7|8|9)", ciphertext))

	index = 0
	while index < len(ciphertext):
		char = ciphertext[index]
		if char == "D": # D means that the following character is duplicated
			plainChar = tryForMappedCharDecrypt(ciphertext[index+1])
			if plainChar not in decrypt_polymappings.keys(): # leave as uppercase if in polymappings, will need further processing
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

	# go through mappings, in order, replacing plaintext character with its cipher counterpart
	alphabet = list(encrypt_ngrams.keys()) + list(encrypt_polymappings.keys()) + list(encrypt_mapping.keys())
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
	elif len(sys.argv) > 1 and "-d" in sys.argv:
		if len(sys.argv) < 3 and not stdinput:
			print("Please provide ciphertext to decrypt.")
		else:
			if stdinput:
				code = sys.stdin.read()
			else:
				code = sys.argv[[i for i, s in enumerate(sys.argv) if '-d' in s][0]+1]
			print(decrypt(code, "-n" in sys.argv))
	else:
		if stdinput:
			code = sys.stdin.read()
		else:
			code = sys.argv[1]
		print(encrypt(code))
