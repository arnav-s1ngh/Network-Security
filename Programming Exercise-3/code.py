import gmpy2
import time
import random
import math
import hashlib
# Reference:- https://github.com/arnav-s1ngh/Foundations-of-Computer-Security/blob/main/Assignment-1/q1.py
def generate_rsa_keys():
    p=gmpy2.next_prime(random.getrandbits(2048))
    q=gmpy2.next_prime(random.getrandbits(2048))
    n=p*q
    phi=(p-1)*(q-1)
    e=65537
    d=gmpy2.invert(e,phi)
    return [[n,e],[n,d]]
def encryption_rsa(msg,pubk):
    n=pubk[0]
    e=pubk[1]
    msg_encoded=int.from_bytes(msg.encode(),'big')
    return gmpy2.powmod(msg_encoded,e,n)
def decryption_rsa(ciphertext,privk):
    n=privk[0]
    d=privk[1]
    msg_encoded=gmpy2.powmod(ciphertext,d,n)
    return msg_encoded.to_bytes(math.ceil(msg_encoded.bit_length()/8),'big').decode()

class certificate_authority:
    def __init__(self,duration,certificate_authority_id):
        self.certificates={}
        self.certificate_authority_id=certificate_authority_id
        self.pubk,self.privk=generate_rsa_keys()
        self.duration=duration
    def create_certificate(self,client_id,client_pubk):
        time_of_issuance=int(time.time())
        certificate_data=f"{client_id},{client_pubk[0]},{client_pubk[1]},{time_of_issuance},{self.duration},{self.certificate_authority_id}"
        hashed_certificate_data=hashlib.sha256(certificate_data.encode()).hexdigest()
        encrypted_hashed_certificate_data=encryption_rsa(hashed_certificate_data,self.privk)
        self.certificates[client_id]=[certificate_data,encrypted_hashed_certificate_data]
        return [certificate_data,encrypted_hashed_certificate_data]
    def get_certificate(self,client_id):
        if client_id not in self.certificates.keys():
            return None
        return self.certificates[client_id]


class client:
    def __init__(self,client_id,cert_authority):
        self.client_id=client_id
        self.pubk,self.privk=generate_rsa_keys()
        self.cert_authority=cert_authority
        self.cert=None
        self.inbox=[]
        self.cont=[]
    def get_your_certificate(self):
        crt=self.cert_authority.create_certificate(self.client_id,self.pubk)
        if self.validate_certificate(crt,self.client_id)==True:
            print("Valid Self-Cert received from CA.")
        else:
            print("Invalid Cert obtained, Try Again.")
            exit()
        self.cert=crt[0]
        print(self.cert)
        return self.cert
    def get_other_certificate(self,other_id):
        other_cert=self.cert_authority.get_certificate(other_id)
        if self.validate_certificate(other_cert,other_id)==True:
            print("Valid Other-Cert received from CA.")
        else:
            print("Invalid Other-Cert obtained, Try Again.")
            exit()
        print(other_cert[0])
        return other_cert
    def send_msg(self,sender,message,receiver_pubk,receiver):
        encrypted_msg=encryption_rsa(message,receiver_pubk)
        receiver.inbox.append(encrypted_msg)
        receiver.cont.append(sender.client_id)
        print("The follwing message is being sent from", sender.client_id, "to", receiver.client_id)
        print("Encrypted Message:", encrypted_msg)
    def receive_msg(self):
        decrypted_message=decryption_rsa(self.inbox[len(self.inbox)-1],self.privk)
        sender_identity=self.cont[len(self.inbox)-1]
        print("The following message was received by",self.client_id, "from", sender_identity)
        print("Decrypted Message:", decrypted_message)
    def validate_certificate(self,crt,cid):
        if crt==None:
            print("Certificate is Invalid: Null Value")
            return False
        if decryption_rsa(crt[1],self.cert_authority.pubk)==hashlib.sha256(crt[0].encode()).hexdigest():
            print("No Tampering Detected")
            cert_list=crt[0].split(",")
            toi=cert_list[3]
            dur=cert_list[4]
            if int(toi)<=int(time.time())<int(toi)+int(dur):
                print("Certificate has not expired")
                if cert_list[0]==cid:
                    print("Certificate ID matches actual ID")
                    return True
            else:
                print("Certificate has expired")
        return False


cert_auth=certificate_authority(duration=1,certificate_authority_id=10001)
client_alice=client("Alice",cert_auth)
client_bob=client("Bob",cert_auth)
print("\nClients request their own certificates\n")
client_alice.get_your_certificate()
client_bob.get_your_certificate()
print("\nClients request the other guy's certificate\n")
cert_alice=client_bob.get_other_certificate("Alice")
cert_bob=client_alice.get_other_certificate("Bob")
pubk_alice=(int(cert_alice[0].split(",")[1]),int(cert_alice[0].split(",")[2]))
pubk_bob=(int(cert_bob[0].split(",")[1]),int(cert_bob[0].split(",")[2]))

print(f"\nClient Bob obtained Alice's public key:",pubk_alice,"\n")
print(f"\nClient Alice obtained Bob's public key:",pubk_bob,"\n")

print("\nClients exchange messages")
messages_from_a = ["Hello1", "Hello2", "Hello3"]
messages_from_b = ["ACK1", "ACK2", "ACK3"]

client_alice.send_msg(client_alice,"Hello1",pubk_bob,client_bob)
client_bob.receive_msg()
client_alice.send_msg(client_alice,"Hello2",pubk_bob,client_bob)
client_bob.receive_msg()
client_alice.send_msg(client_alice,"Hello3",pubk_bob,client_bob)
client_bob.receive_msg()

client_bob.send_msg(client_bob,"ACK1",pubk_alice,client_alice)
client_alice.receive_msg()
client_bob.send_msg(client_bob,"ACK2",pubk_alice,client_alice)
client_alice.receive_msg()
client_bob.send_msg(client_bob,"ACK3",pubk_alice,client_alice)
client_alice.receive_msg()

print("\nProgram Executed Successfully\n")
