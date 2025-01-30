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

#Brute Force Attack
ipt=input("Select Input Type 'binary' or 'alphabetical' ")
if ipt=="binary":
    intercepted_text=input("Intercepted Text:- ")
    for i in intercepted_text:
        if i not in ["0","1"] or len(intercepted_text)%3!=0:
            print("Illegal Input Detected")
            exit()
    intercepted_text=bintotext(intercepted_text)
elif ipt=="alphabetical":
    intercepted_text=input("Intercepted Text:- ")
    for i in intercepted_text:
        if i not in universal_set:
            print("Illegal Input Detected")
            exit()
else:
    print("Illegal Input Detected")
    exit()
start_time=time.time()
possible_keys=permutations(universal_set, 8)
possible_keys=[''.join(p) for p in possible_keys]
for possible_key in possible_keys:
    fmap={}
    for i in range(len(universal_set)):
        fmap[possible_key[i]]=universal_set[i]
    temp_text="".join([fmap[i] for i in [j for j in intercepted_text]])
    pure_text=temp_text[0:len(temp_text)-11]
    hash_text=temp_text[len(temp_text)-11:]
    if hash_fnv1a(pure_text)==texttobin(hash_text):
        print("Succcess")
        print(pure_text)
        print("Elapsed Time",time.time()-start_time)
