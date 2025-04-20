# Client Side Application
from time import sleep
import requests
import fitz
import hashlib
import rsa
def hash_function(pth):
    file=fitz.open(pth)
    file_text=""
    for pg in file:
        file_text+=pg.get_text()
    file.close()
    print(f"File Content:- {file_text}")
    file_hash=hashlib.sha256(file_text.encode('utf-8')).hexdigest()
    print(f"File Hash:- {file_hash}")
    return file_hash
# hash_function("document.pdf")
def verify_signature(pdf_hash,timestamp,signature,public_key):
    try:
        message=f"{pdf_hash}|{timestamp}".encode('utf-8')
        rsa.verify(message,signature,public_key)
        print("Signature is valid")
        return True
    except rsa.VerificationError:
        print("Signature is invalid")
        return False
def add_timestamp_to_pdf(pth,timestamp,sig):
    doc=fitz.open(pth)
    f_page=doc[0]
    f_page.insert_textbox(fitz.Rect(20, 20, 500, 100),f"Signature: {sig}\nTimestamp: {timestamp}",fontsize=2,color=(0.999,0.4,0.5))
    new_file_loc=pth.replace(".pdf","_stamped.pdf")
    doc.save(new_file_loc)
    print(f"\nThe timestamped pdf was saved at:- {new_file_loc}\n")
    doc.close()
# add_timestamp_to_pdf("document.pdf","16:43","Joan Holloway Harris")
def client_server_channel():
    print("Client Program Initialising")
    sleep(1)
    print("\nNote:- This program is only capable of processing PDFs\n")
    file_name=input("Enter the path for the file you wish to have time-stamped:- ")
    file_hash=hash_function(file_name)
    print(f"\nSending hash {file_hash} to timestamping server")
    response=requests.post("https://localhost:5000/timestamp", json={"hash":file_hash}, verify="cert.pem")
    if response.status_code==200:
        print("\nRequest executed successfully\n")
        result=response.json()
        timestamp=result["timestamp"]
        print(timestamp)
        signature=result["signature"]
        print(signature)
        print(result["public_key"])
        if verify_signature(file_hash,timestamp,bytes.fromhex(signature),rsa.PublicKey.load_pkcs1((result["public_key"]).encode('utf-8'))):
            add_timestamp_to_pdf(file_name, timestamp, signature)
        else:
            print("Validation Failed. Aborting")
            exit()
    else:
        print("Request failed gracefully")
        print(response.status_code)
client_server_channel()
