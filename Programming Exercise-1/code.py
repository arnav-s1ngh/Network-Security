#Transposition Cipher
import string
from time import sleep
import math
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
# guinea="abcd"
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
print("Plaintext is acceptable\n")
key_size=int(input("Key Size [less than or equal to 9]:- "))
if not (key_size>=0 and key_size<=9):
    print("Illegal Input. Exiting Safely.")
    exit()
sleep(1)
print("Key Size is acceptable\n")
key=input("Enter the key without any spaces:- ")
if len(key)!=key_size or not set([i for i in key]).issubset(set(["1","2","3","4","5","6","7","8","9"])):
    print("Illegal Input. Exiting Safely.")
    exit()
sleep(1)
print("Key is acceptable\n")
plaintext+=hash_fnv1a(plaintext)
# print(plaintext)
# Number of Columns in the table == key_size
# Number of Rows in the table == ceil(len(concatenatedtext)/key_size)
# print("Padding Size:- ", (key_size*math.ceil(len(plaintext)/key_size)-len(plaintext)))
table=[['q']*key_size for i in range(math.ceil(len(plaintext)/key_size))]
for i in range(len(plaintext)):
    table[i//key_size][i%key_size]=plaintext[i]
key=[int(i) for i in key]
indices=list(range(len(table[0])))
indices.sort(key=lambda x:key[x])
cipher_text=""
for i in indices:
    for rownum in range(len(table)):
        cipher_text+=str(table[rownum][i])
print("Sent Cipher:- ", cipher_text,"\n")
print("The plaintext has been successfully encrypted\n")

#Decryption
print("Decryption Initiated")
received_text=input("Cipher Text:- ")
received_key=int(input("Enter the key without any spaces:- "))



#Brute Force Attack
