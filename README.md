# keyless-vigenere-decrypter
Decrypts a vigenere cipher encrypted text file without a key.

It decodes the text by first finding the length of this key.
This is done by finding the difference between peaks in 'coincidences' in the text.
A coincidence is where the same letter appears in the same index as the original text to when it has been shifted.

After it has the key length it then splits the text into the sections which have been shifted by the same key.
It then performs a frequency distribution analysis using the chi square method to determine which shift most closely reflects
the distribution of the english alphabet. This is repeated for all the letters in the key until the key has been decoded

It is then able to shift the letters back to plaintext using the key and code.
