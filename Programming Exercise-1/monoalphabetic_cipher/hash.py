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

def hash_fnv1a(s):
    hash=0x811c9dc5
    for x in s:
        hash=((ord(x)^hash)* 0x01000193) & 0xFFFFFFFF
    hash=str(bin(hash)[2:])
    if len(hash)<33:
        hash="0"*(33-len(hash))+hash
    return hash #output in 1s and 0s
print("Enter Input Type:-\n1.Binary\n2.Alphabetical")
ques=input("---> ")
if ques=="1" or ques.lower()=="binary":
    inp=input("Input:- ")
    for i in inp:
        if i not in ["0","1"] or len(inp)%3!=0:
            print(i=="1")
            print(type(i))
            print("Illegal Input Detected")
            exit()
    inp=bintotext(inp)
    print("The hash value for the input is", hash_fnv1a(inp), "i.e.", bintotext(hash_fnv1a(inp)))
    exit()
if ques=="2" or ques.lower()=="alphabetical":
    inp=input("Input:- ")
    for i in inp:
        if i not in universal_set:
            print("Illegal Input Detected")
            exit()
    print("The hash value for the input is ", hash_fnv1a(inp), "i.e.", bintotext(hash_fnv1a(inp)))
    exit()
