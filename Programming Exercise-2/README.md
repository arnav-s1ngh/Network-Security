## References


- [Technical Explanation of DES (TU Berlin)](https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm)  
- [GeeksforGeeks - Data Encryption Standard (DES)](https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/)

---

## Test Cases

### Test Case 1
- **Message:** `0000000000000000`  
- **Key:** `0123456789ABCDEF`  
- **Encrypted Output:** `D5D44FF720683D0D`  
- **Decrypted Output:** `0000000000000000`  

### Test Case 2
- **Message:** `FEDCBA9876453210`  
- **Key:** `BED1FAC032456879`  
- **Encrypted Output:** `3E0A9DC6C6D17B38`  
- **Decrypted Output:** `FEDCBA9876453210`  

### Test Case 3
- **Message:** `FFFFFFFFFFFFFFFF`  
- **Key:** `DEB872CAF1345690` *(Invalid key length; expected 16 hex characters)*  
- **Encrypted Output:** `EEB393885E252560`  
- **Decrypted Output:** `FFFFFFFFFFFFFFFF`

Note: The program can accept shorter inputs, but they are ultimately padded with '0's  
