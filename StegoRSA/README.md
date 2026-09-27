# StegoRSA - picoCTF

## Challenge
RSA private key hidden in image metadata.

## Tools
exiftool, xxd, openssl

## Steps
1. exiftool image.jpg → found hex in Comment
2. xxd -r -p key.hex > private.pem
3. openssl pkeyutl -decrypt -inkey private.pem -in flag.enc

## Flag
academy{rs4_k3y_1n_1mg_9db27b2c

## Learned
Hex can be reversed into binary files. Metadata can hide keys.
