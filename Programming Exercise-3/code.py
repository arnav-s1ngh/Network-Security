import gmpy2
import time
import random


class RSA:
    def __init__(self, bits=1024):
        self.p = gmpy2.next_prime(random.getrandbits(bits // 2))
        self.q = gmpy2.next_prime(random.getrandbits(bits // 2))
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 65537
        self.d = gmpy2.invert(self.e, self.phi)

    def encrypt(self, message, public_key):
        n, e = public_key
        message_int = int.from_bytes(message.encode(), 'big')
        return gmpy2.powmod(message_int, e, n)

    def decrypt(self, ciphertext):
        message_int = gmpy2.powmod(ciphertext, self.d, self.n)
        return message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode()

    def get_public_key(self):
        return (self.n, self.e)


class CertificationAuthority:
    def __init__(self):
        self.rsa = RSA()
        self.certificates = {}

    def issue_certificate(self, client_id, client_public_key):
        timestamp = int(time.time())
        duration = 3600  # Valid for 1 hour
        certificate_data = f"{client_id},{client_public_key[0]},{client_public_key[1]},{timestamp},{duration}"
        encrypted_certificate = self.rsa.encrypt(certificate_data, (self.rsa.n, self.rsa.d))
        self.certificates[client_id] = encrypted_certificate
        return encrypted_certificate

    def get_certificate(self, client_id):
        return self.certificates.get(client_id, None)


class Client:
    def __init__(self, client_id, ca):
        self.client_id = client_id
        self.rsa = RSA()
        self.ca = ca
        self.cert = None

    def request_certificate(self):
        self.cert = self.ca.issue_certificate(self.client_id, self.rsa.get_public_key())

    def get_peer_certificate(self, peer_id):
        return self.ca.get_certificate(peer_id)

    def send_message(self, message, recipient_public_key):
        encrypted_message = self.rsa.encrypt(message, recipient_public_key)
        return encrypted_message

    def receive_message(self, encrypted_message):
        decrypted_message = self.rsa.decrypt(encrypted_message)
        return decrypted_message


# Simulating the process
ca =  CertificationAuthority()
client_a = Client("A", ca)
client_b = Client("B", ca)

client_a.request_certificate()
client_b.request_certificate()

cert_b = client_a.get_peer_certificate("B")
if cert_b:
    print("Client A received certificate for B")
    message = "Hello, B!"
    encrypted_msg = client_a.send_message(message, client_b.rsa.get_public_key())
    received_msg = client_b.receive_message(encrypted_msg)
    print("Client B received message:", received_msg)
