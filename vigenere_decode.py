"""
Vigenere decoder

Takes in a vigenere encrypted text file, finds the key and decrypts the text.

It decodes the text by first finding the length of this key.
This is done by finding the difference between peaks in 'coincidences' in the text.
A coincidence is where the same letter appears in the same index as the original text to when it has been shifted.

After it has the key length it then splits the text into the sections which have been shifted by the same key.
It then performs a frequency distribution analysis using the chi square method to determine which shift most closely reflects
the distribution of the english alphabet. This is repeated for all the letters in the key until the key has been decoded

It is then able to shift the letters back to plaintext using the key and code.
"""

import math


"""
Shifts code to the right by shift amount of spaces
Inputs:
List code - code to shift
Int shift - amount to shift code by

Outputs:
List rot - code after it has been shifted
"""
def rotate(code, shift):
    return([" " for i in range(shift)] + [i for i in code[0:len(code) - shift]])


"""
Finds length of key
Inputs:
List code - the encrypted text to find key length of

Outputs:
Int length - the length of the key
""" 
def find_key_length(code):
    codeLen = len(code)

    # Generates all right shifts of code
    rotations = [rotate(code, i) for i in range(1, codeLen)]

    print(rotations)
    
    # Counts the amount of times that letters appear in the same position as the original code
    coincidences = []
    for rotation in rotations:
        coincidence = 0
        for j in range(len(rotations) + 1):
            if code[j] == rotation[j]:
                coincidence += 1
        
        coincidences.append(coincidence)

    print(coincidences)

    # Determines where there's a peak in the data
    peaks = []
    difference_allowed = 10
    for i in range(1, len(coincidences)-1):
        if (coincidences[i+1] - coincidences[i] <= -difference_allowed) and (coincidences[i] -  coincidences[i-1] >= difference_allowed):
            peaks.append(i+1)
    
    # Finds the most common differences between the peaks
    gcd = []
    for i in range(1, len(peaks)):
        factor = math.gcd(peaks[i], peaks[i-1])
        if factor > 2:
            gcd.append(factor)
    
    length = max(gcd, key=gcd.count)
    
    return length


"""
Finds key using chi square formula
Inputs:
List code - encrypted text to find key of
Int length - length of key

Outputs:
String key - the key of the code
"""
def chi_square(code, length):
    # Splits the code into the sections which have been shifted by the same key
    split = [code[i::length] for i in range(length)]

    # Expected letter frequencies for english
    frequencies = {
        "a": 0.08497,
        "b": 0.01492,
        "c": 0.02202,
        "d": 0.04253,
        "e": 0.11162,
        "f": 0.02228,
        "g": 0.02015,
        "h": 0.06094,
        "i": 0.07546,
        "j": 0.00153,
        "k": 0.01292,
        "l": 0.04025,
        "m": 0.02406,
        "n": 0.06749,
        "o": 0.07507,
        "p": 0.01929,
        "q": 0.00095,
        "r": 0.07587,
        "s": 0.06327,
        "t": 0.09356,
        "u": 0.02758,
        "v": 0.00978,
        "w": 0.02560,
        "x": 0.00150,
        "y": 0.01994,
        "z": 0.00077
    }

    key = ""

    # Finds the chi square value of each shift
    # The smallest chi square is the closest to english
    for group in split:
        chi_count = []
        shift_len = len(group)

        letter_frequency = {i : group.count(i)/shift_len for i in set(group)}
        
        
        for shift in range(26):
            chi_square_value = 0
            for i in letter_frequency:
                new_index = ((ord(i) - ord("a")) - shift) % 26
                new_character = chr(new_index + ord("a"))

                chi_square_value += (letter_frequency[i] - frequencies[new_character])**2/frequencies[new_character]
            chi_count.append(chi_square_value) 

        key += chr(ord("a") + chi_count.index(min(chi_count)))

    return key


"""
Decodes code using key
Inputs:
List code - The code to be decoded
String key - The key to be used for decoding

Output:
String decoded - The decoded text
"""
def decode(code, key):

    key_length = len(key)
    decoded = ''
    for i in range(len(code)):
        value = (ord(code[i]) - ord(key[i % key_length])) % 26
        decoded += chr(value + ord("a"))

    return decoded


"""
Reformats the decoded text to ensure the punctuation matches the original grammar
Inputs:
String old_text - original encoded text
String decoded - unformatted decoded text

Outputs:
String formatted - formatted decoded text with proper punctuation
"""
def reformat(old_text, decoded):
    formatted = ""
    count = 0

    for i in old_text:
        if not i.isalpha():
            formatted += i
        else:
            if i.isupper():
                formatted += decoded[count].upper()
            else:
                formatted += decoded[count]
            count += 1

    return(formatted)
                

def main():
    user = input("Enter file path: ")
    with open(user, "r", encoding='utf-8') as f:
        code = f.read()

        formatted_code = [i.lower() for i in code if i.isalpha()]

        length = find_key_length(formatted_code)
        
        key = chi_square(formatted_code, length)
        print("\nKEY:", key)
        
        decoded = decode(formatted_code, key)

        reformatted = reformat(code, decoded)
        print("\n" + reformatted)

if __name__ == "__main__":
    main()

# File names and expected key
# alice - dragons
# garlic - cookie
# piano - longerpassword
# voices - cat
# frankenstein - monster
