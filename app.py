from flask import Flask,jsonify,request,abort
import json

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.fernet import Fernet

def genKey(password_provided):
    password = password_provided.encode() 
    salt = b'rrdX9A66qXtQZwzf' # You NEED TO CHANGE THIS (eg. os.urandom(16)) must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    return key

app = Flask(__name__)

'''
Secure Transport (TLS) is mandatory.
This snippet is minimalist on purpose so to keep processing on the memory
'''
@app.route("/", methods=('GET',))
def hello():
    return "App is Up!"


@app.route("/encrypt", methods=['POST'])
def encrypt():
    '''
    {
        "key":"secretKey",
        "plaintext":"Text containing sensitive data to be encrypted"
    }
    '''
    req_data = request.get_json()

    try:
        key = req_data['key']
        plaintext = req_data['plaintext']
    except:
        abort(400)

    message = plaintext.encode()

    try:
        f = Fernet(genKey(key))
        encrypted = f.encrypt(message)
    except:
        abort(403)
    
    return json.dumps({'ciphertext':encrypted.decode()})
     

@app.route("/decrypt", methods=['POST'])
def decrypt():
    '''
    {
        "key":"secretKey",
        "ciphertext":"gAAAAABdGQQgxejDKPqkR9tMGdHsL0ewJr3z3TOZeNC7-0AxBIxCv3gjAmng4ZrIY668ovifRMl1_F_5O64Wjbhn0qsm2Vn7UjbEhOEvXFlFIaK1ichVONWHr0sMGD5s30TNf7_9LEKN"
    }
    '''
    req_data = request.get_json()
    try:
        key = req_data['key']
        ciphertext = req_data['ciphertext']
    except:
        abort(400)

    encrypted = ciphertext.encode()
    
    try:
        f = Fernet(genKey(key))
        decrypted = f.decrypt(encrypted)
    except:
        abort(403)

    return json.dumps({'plaintext':decrypted.decode()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)