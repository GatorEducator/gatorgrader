"""
File to illustrate how bitcoin addresses are used.
Name: Jordan Byrne
"""

# pip install base58, ecdsa
import bitcoin
import hashlib, base58, binascii, codecs, ecdsa

# Step 1: generate private key
privateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
print("Private Key: ", privateKey.to_string().hex())

# step 2: Generate a public key
# elipctic curve multiplication. From a value to a point on a curve. (04 means uncompressed key)
publicKey = "04" + privateKey.get_verifying_key().to_string().hex()
print("Public Key: ", publicKey)

# step 3: get hash
hash = hashlib.sha256(binascii.unhexlify(publicKey)).hexdigest
print("Hash", hash)

# step 4: apply RIDEMP160
ride = hashlib.new('ripemd160', binascii.unhexlify(hash))
print("Rip: ", rip)

# step 5: prepend 00 as network byte  (00 value indicates main network.)
prepend = '00' + rip

# step 6: Apply double hash
hash1 = prepend
for i in range(1, 3):
    hash1 = hashlib.sha256(binascii.unhexlify(hash1).hexdigest())

# Step 7: get checksum
checksum = hash1[:8]

appendChecksum = prepend + checksum

# Step 8: generate address.
address = base58.b58encode(binascii.unhexlify(appendChecksum))
print("Bitcoin Address:", address.decode('utf8'))
