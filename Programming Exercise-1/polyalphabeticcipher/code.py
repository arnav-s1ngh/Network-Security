#Poly-Alphabetic Cipher
import string
import time
from time import sleep
import math
from itertools import permutations

universal_set=list(string.ascii_lowercase)
# Hashing
# Reference:- https://gist.github.com/amakukha/7854a3e910cb5866b53bf4b2af1af968
# Initially used djb2, but as pointed out on this webpage ☝️, it suffers from avalanching
def hash_fnv1a(s):
    hash=0x811c9dc5
    for x in s:
        hash=((ord(x)^hash)* 0x01000193) & 0xFFFFFFFF
    hash="".join([universal_set[int(i)] for i in str(hash)])
    if len(hash)<10:
        hash+=(10-len(hash))*"y"
    return hash
guinea="abcd"
# print(hash_fnv1a(guinea))
# print(len(str(hash_fnv1a(guinea))))
# print(len(guinea))

#Encryption
print("Encryption Initiated....\n")
plaintext=input("Original Text:- ")
if not set([i for i in plaintext]).issubset(set(universal_set)):
    print("Illegal Input. Exiting Safely.")
    exit()
sleep(1)
print("Original Text is acceptable\n")
print(hash_fnv1a(plaintext))
key_size=4
print("Key Size is acceptable\n")
key=input("Enter the key without any spaces:- ")
for i in key:
    if i not in universal_set:
        print("Illegal Symbols Detected")
        exit()
sleep(1)
print("Key is acceptable\n")
plaintext+=hash_fnv1a(plaintext)
key=[i for i in key]
add=[int(universal_set.index(i)) for i in key]
add_key=add*(int(len(plaintext)//len(key)))+add[0:(len(plaintext)%len(key))]
print(len(plaintext))
print(len(add_key))
cipher_text=[universal_set[(universal_set.index(plaintext[i])+add_key[i])%26] for i in range(len(plaintext))]
cipher_text="".join(cipher_text)
print("Sent Cipher:- ", cipher_text,"\n")
print("The plaintext has been successfully encrypted\n")

#Decryption
given_text=input("Cipher Text:- ")
given_key=input("Key:- ")
given_key=[i for i in given_key]
add=[int(universal_set.index(i)) for i in given_key]
add_key=add*(int(len(given_text)//len(given_key)))+add[0:(len(given_text)%len(given_key))]
cipher_text=[universal_set[(26+universal_set.index(given_text[i])-add_key[i])%26] for i in range(len(given_text))]
cipher_text="".join(cipher_text)
rec_text=cipher_text[0:len(cipher_text)-10]
hash_text=cipher_text[len(cipher_text)-10:len(cipher_text)]
if hash_fnv1a(rec_text)!=hash_text:
    print("Received Data is corrupted.")
    exit()
print("Received Plaintext:- ", rec_text,"\n")
print("The cipher has been successfully decrypted\n")

#Brute Force Attack
given_text=input("Cipher Text:- ")
start_time=time.time()
possible_keys=permutations(universal_set+universal_set+universal_set+universal_set, 4)
possible_keys=[''.join(p) for p in possible_keys]
# print(possible_keys)
for possible_key in possible_keys:
    given_key=possible_key
    given_key=[i for i in given_key]
    add=[int(universal_set.index(i)) for i in given_key]
    add_key=add*(int(len(given_text)//len(given_key)))+add[0:(len(given_text)%len(given_key))]
    cipher_text=[universal_set[(26+universal_set.index(given_text[i])-add_key[i])%26] for i in range(len(given_text))]
    cipher_text="".join(cipher_text)
    rec_text = cipher_text[0:len(cipher_text) - 10]
    hash_text = cipher_text[len(cipher_text) - 10:len(cipher_text)]
    if hash_fnv1a(rec_text)==hash_text:
        print("Plaintext:- ", rec_text, "\n")
        print("Time to crack", time.time() - start_time)
        exit()


