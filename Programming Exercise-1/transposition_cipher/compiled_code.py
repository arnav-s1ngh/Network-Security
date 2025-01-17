#Transposition Cipher
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
print("Original Text is acceptable\n")
print(hash_fnv1a(plaintext))
key_size=int(input("Key Size [less than or equal to 9]:- "))
if not (key_size>=1 and key_size<=9):
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
received_key=(input("Enter the key without any spaces:- "))
received_key=[i for i in received_key]
num_rows=int(len(received_text)/len(received_key))
table2=[['a']*len(received_key) for i in range(num_rows)]
indices=list(range(len(received_key)))
indices.sort(key=lambda x:received_key[x])
idx=0
for i in range(len(received_text)):
    table2[i%num_rows][indices[idx]]=received_text[i]
    if i%num_rows==num_rows-1:
        idx+=1
impure_string="".join(["".join(i) for i in table2])

i=len(impure_string)-1
#Removing Padding (if any)
while impure_string[i]=="q":
    i-=1
impure_string=impure_string[0:i+1]

#Removing Hash and verifying authenticity
pure_string=impure_string[0:len(impure_string)-10]
hash_string=impure_string[len(impure_string)-10:len(impure_string)]
if hash_fnv1a(pure_string)!=hash_string:
    print("The Encryption has been breached. We have been compromised")
    print(pure_string)
    print(hash_string)
    exit()
else:
    print("Hash Successfully Verified")
    sleep(1)
    print("The Received Text:- ", pure_string)

#Brute Force Attack
attackcipher=input("Cipher Text:-")
start_time=time.time()
compatiblekeys=[i for i in range(1,10) if len(attackcipher)%i==0]
for key in compatiblekeys:
    possiblekeys=["".join(p) for p in permutations("".join([str(x) for x in list(range(1,key+1))]))]
    for j in possiblekeys:
        j="".join(j)
        j=[st for st in j]
        num_rows=int(len(attackcipher)/len(j))
        table2=[['a'] * len(j) for i in range(num_rows)]
        indices=list(range(len(j)))
        indices.sort(key=lambda x: j[x])
        idx=0
        for i in range(len(attackcipher)):
            table2[i%num_rows][indices[idx]]=attackcipher[i]
            if i%num_rows==num_rows-1:
                idx+=1
        impure_string="".join(["".join(i) for i in table2])

        i=len(impure_string)-1
        # Removing Padding (if any)
        while impure_string[i]=="q":
            i-=1
        impure_string=impure_string[0:i+1]

        # Removing Hash and verifying authenticity
        pure_string=impure_string[0:len(impure_string)-10]
        hash_string=impure_string[len(impure_string)-10:len(impure_string)]
        if hash_fnv1a(pure_string)!=hash_string:
            pass
        else:
            print("Hash Successfully Verified")
            sleep(1)
            print("The Received Text:- ", pure_string)
            print("Time Elapsed ",time.time()-start_time, " seconds.")
            exit()
