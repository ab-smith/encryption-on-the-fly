from flask import Flask,jsonify,request,abort
from flask_restplus import Resource, Api, fields, reqparse
import json

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.fernet import Fernet


flask_app = Flask(__name__)
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "EOF (Encryption On the Fly)", 
		  description = "Manage real-time encryption for your app with a simple API. Based on Fernet implementation which uses 128-bit AES in CBC mode and PKCS7 padding, with HMAC using SHA256. Proof Of Concept API with NO INFORMATION STORED.")

name_space = app.namespace('v1', description='Encryption on the fly API')


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

'''
Secure Transport (TLS) is mandatory.
This snippet is minimalist on purpose so to keep processing on the memory
'''
EncryptThis = app.model('Encrypt This', {
    'key': fields.String(required=True, description='Your encryption password that will be used to derivate the key'),
    'plaintext': fields.String(required=True, description='Data to encrypt')
})

DecryptThis = app.model('Decrypt This', {
    'key': fields.String(required=True, description='Your encryption password used to derivate the key'),
    'ciphertext': fields.String(required=True, description='Data to decrypt')
})

@name_space.route('/health')
class Health(Resource):
    def get(self):
        '''Return system health status'''
        return {'status': 'Everything looks fine'}

                                       
@name_space.route('/encrypt')
class Encryption(Resource):
    '''
    {
        "key":"secretKey",
        "plaintext":"Text containing sensitive data to be encrypted"
    }
    '''
    @name_space.expect(EncryptThis)
    def post(self):
        '''Get a plaintext and the associated key and return ciphertext'''
        try:
            key = name_space.payload['key']
            plaintext = name_space.payload['plaintext']
        except:
            abort(400)
        
        message = plaintext.encode()
        
        try:
            f = Fernet(genKey(key))
            encrypted = f.encrypt(message)
        except:
            abort(403)
        
        return {'ciphertext':encrypted.decode()}

@name_space.route('/decrypt')
class Decryption(Resource):
    '''
    {
        "key":"secretKey",
        "ciphertext":"gAAAAABdGQQgxejDKPqkR9tMGdHsL0ewJr3z3TOZeNC7-0AxBIxCv3gjAmng4ZrIY668ovifRMl1_F_5O64Wjbhn0qsm2Vn7UjbEhOEvXFlFIaK1ichVONWHr0sMGD5s30TNf7_9LEKN"
    }
    '''
    @name_space.expect(DecryptThis)
    def post(self):
        '''Get a ciphertext and the associated key and return plaintext'''
        try:
            key = name_space.payload['key']
            ciphertext = name_space.payload['ciphertext']
        except:
            abort(400)

        encrypted = ciphertext.encode()
        
        try:
            f = Fernet(genKey(key))
            decrypted = f.decrypt(encrypted)
        except:
            abort(403)

        return {'plaintext':decrypted.decode()}

if __name__ == '__main__':
    flask_app.run(debug=False)