def cryptageCypher(message, key):
    encrypted = ""
    for i in range(len(message)):
        character = message[i]
        if character.isalpha():
            if character.isupper():
                encrypted += chr((ord(character) + key - 65) % 26 + 65)
            else:
                encrypted += chr((ord(character) + key - 97) % 26 + 97)
        else:
            encrypted += character
    return encrypted

def decryptageCypher(message, key):
    return cryptageCypher(message, -key)

text = "Yasmina teste le cryptage de César"
key = 5
encrypted = cryptageCypher(text, key)
decrypted = decryptageCypher(encrypted, key)

print("Texte original:", text)
print("Texte crypté:", encrypted)
print("Texte décrypté:", decrypted)