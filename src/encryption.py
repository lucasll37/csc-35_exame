import pickle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Classe exemplo para demonstração
class MyClass:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"MyClass(name={self.name}, value={self.value})"

# Função para gerar uma chave simétrica aleatória
def generate_symmetric_key():
    return os.urandom(32)  # Gera uma chave aleatória de 256 bits (32 bytes)

# Função para criptografar o objeto
def encrypt_object(key, obj):
    serialized_obj = pickle.dumps(obj)  # Serializar o objeto em bytes
    iv = os.urandom(16)  # Gera um vetor de inicialização aleatório
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(serialized_obj) + encryptor.finalize()
    return iv + ciphertext  # Retornar IV + ciphertext

# Função para descriptografar o objeto
def decrypt_object(key, encrypted_data):
    iv = encrypted_data[:16]  # Extrair o IV
    ciphertext = encrypted_data[16:]  # Extrair o ciphertext
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    serialized_obj = decryptor.update(ciphertext) + decryptor.finalize()
    return pickle.loads(serialized_obj)  # Desserializar o objeto original