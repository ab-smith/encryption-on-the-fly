# Mini Flask App for Data Encrypt/Decrypt

EOF: Encryption On the Fly (not End Of File)

This is a minimalist Flask app that exposes an API for symmetric data encryption.

Three routes are available:

- `/` app status
- `encrypt` get the key and plaintext from the post json payload and return a ciphertext
- `decrypt` get the key and ciphertext from the post json payload and return the original text