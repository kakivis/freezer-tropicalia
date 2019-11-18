from Crypto import Random
from Crypto.PublicKey import RSA
import base64


def generate_keys():
	# key length must be a multiple of 256 and >= 1024
	modulus_length = 256*4
	private_key = RSA.generate(modulus_length, Random.new().read)
	public_key = private_key.publickey()
	return private_key, public_key


def encrypt_message(a_message , public_key):
	encrypted_msg = public_key.encrypt(a_message, 32)[0]
	encoded_encrypted_msg = base64.b64encode(encrypted_msg)
	return encoded_encrypted_msg


def decrypt_message(encoded_encrypted_msg, private_key):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = private_key.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg


if __name__ == '__main__':
	a_message = "This is the illustration of RSA algorithm of asymmetric cryptography"
	private_key, public_key = generate_keys()
	encrypted_msg = encrypt_message(a_message, public_key)
	decrypted_msg = decrypt_message(encrypted_msg, private_key)

	print "%s - (%d)" % (private_key.exportKey(), len(private_key.exportKey()))
	print "%s - (%d)" % (public_key.exportKey(), len(public_key.exportKey()))
	print " Original content: %s - (%d)" % (a_message, len(a_message))
	print "Encrypted message: %s - (%d)" % (encrypted_msg, len(encrypted_msg))
	print "Decrypted message: %s - (%d)" % (decrypted_msg, len(decrypted_msg))