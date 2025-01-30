#Mono-Alphabetic Cipher
import string
import time
from time import sleep
import math
from itertools import permutations

universal_set=["A","B","C","D","E","F","G","H"]
universal_num_set=["000","001","010","011","100","101","110","111"]

# Hashing
# Reference:- https://gist.github.com/amakukha/7854a3e910cb5866b53bf4b2af1af968
# Initially used djb2, but as pointed out on this webpage ☝️, it suffers from avalanching
def hash_fnv1a(s):
    hash=0x811c9dc5
    for x in s:
        hash=((ord(x)^hash)* 0x01000193) & 0xFFFFFFFF
    hash=str(bin(hash)[2:])
    if len(hash)<33:
        hash="0"*(33-len(hash))+hash
    return hash #output in 1s and 0s

def bintotext(s):
    temp = ""
    for i in range(0, len(s), 3):
        temp += universal_set[universal_num_set.index(s[i:i + 3])]
    return temp
def texttobin(s):
    temp=""
    for i in range(len(s)):
        temp+=universal_num_set[universal_set.index(s[i])]
    return temp


#Encryption
print("Encryption Initiated....\n")
binaryortext=input("What is your input type, 'binary', or 'alphabetical'? ")
if binaryortext=='binary':
    plaintext=input("Original Text:- ")
    for j in range(len(plaintext)):
        if (plaintext[j] not in ["0","1"]) or len(plaintext)%3!=0:
            print("Illegal Values")
            exit()
    i=0
    temp=""
    for i in range(0,len(plaintext),3):
        temp+=universal_set[universal_num_set.index(plaintext[i:i+3])]
    plaintext=temp
elif binaryortext=='alphabetical':
    plaintext=input("Original Text:- ")
    for j in range(len(plaintext)):
        if (plaintext[j] not in universal_set):
            print("Illegal Values")
            exit()
else:
    print("Illegal Values Detected")
    exit()

key=input("Enter an alphabetical key that will be mapped to the characters A-H in order:- ")
for i in key:
    if i not in universal_set or len(key)!=len(universal_set) or set(key)!=set(universal_set):
        print("The Entered Key is not satisfactory")
        exit()
print("Key is acceptable\n")
plaintext+=bintotext(hash_fnv1a(plaintext))
hmap={}
for i in range(len(universal_set)):
    hmap[universal_set[i]]=key[i]
print(hmap)
plaintext="".join([hmap[i] for i in [j for j in plaintext]])
print("\nSent Cipher:- ",plaintext)
print("Sent Cipher in Binary:- ", texttobin(plaintext))
