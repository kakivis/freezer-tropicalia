import os

from Crypto import Random
from Crypto.PublicKey import RSA
import base64


class AsymmetricCryptography:
	def __init__(self):
		self.private_key_file_name = 'private_key.pem'
		self.private_key = self.load_private_key_from_file()

	def load_private_key_from_file(self):
		if not os.path.exists(self.private_key_file_name):
			file = open(self.private_key_file_name, 'w+')
			modulus_length = 256 * 4
			private_key = RSA.generate(modulus_length, Random.new().read)
			file.write(private_key.exportKey())
			file.close()
			return private_key
		file = open(self.private_key_file_name, 'r')
		key_str = file.read()
		private_key = RSA.importKey(key_str)
		file.close()
		return private_key

	def generate_public_key(self, public_key_file_name):
		if os.path.exists(public_key_file_name):
			exit("ERROR 02 - PROVIDED PUBLIC KEY FILE NAME ALREADY EXISTS")
		file = open(public_key_file_name, 'w+')
		public_key = self.private_key.publickey()
		file.write(public_key.exportKey())
		file.close()
		return public_key

	@staticmethod
	def encrypt_message(message, public_key):
		encrypted_msg = public_key.encrypt(message, 32)[0]
		encoded_encrypted_msg = base64.b64encode(encrypted_msg)
		return encoded_encrypted_msg

	def decrypt_message(self, encoded_encrypted_msg):
		decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
		decoded_decrypted_msg = self.private_key.decrypt(decoded_encrypted_msg)
		return decoded_decrypted_msg

# def generate_keys():
# 	# key length must be a multiple of 256 and >= 1024
# 	modulus_length = 256*4
# 	private_key = RSA.generate(modulus_length, Random.new().read)
# 	public_key = private_key.publickey()
# 	return private_key, public_key


def encrypt_message(message, public_key):
	encrypted_msg = public_key.encrypt(message, 32)[0]
	encoded_encrypted_msg = base64.b64encode(encrypted_msg)
	return encoded_encrypted_msg


def decrypt_message(encoded_encrypted_msg, private_key):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = private_key.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg


if __name__ == '__main__':
	a_message = "This is the illustration of RSA algorithm of asymmetric Cryptography"
	crypt = AsymmetricCryptography()
	a_public_key = crypt.generate_public_key('public_key.pem')
	an_encrypted_msg = crypt.encrypt_message(a_message, a_public_key)
	a_decrypted_msg = crypt.decrypt_message(an_encrypted_msg)

	print "%s - (%d)" % (crypt.private_key.exportKey(), len(crypt.private_key.exportKey()))
	print "%s - (%d)" % (a_public_key.exportKey(), len(a_public_key.exportKey()))
	print " Original content: %s - (%d)" % (a_message, len(a_message))
	print "Encrypted message: %s - (%d)" % (an_encrypted_msg, len(an_encrypted_msg))
	print "Decrypted message: %s - (%d)" % (a_decrypted_msg, len(a_decrypted_msg))
