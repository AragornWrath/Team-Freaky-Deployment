import string
import random

def generateToken(length) :
    extras = "!@#$%^"
    val = ""
    validChars = string.ascii_letters + string.digits
    for letter in range(length) :
        val += random.choice(validChars)
    
    return val

def generateImageToken(length) :
    val = ""
    validChars = string.ascii_letters + string.digits
    for letter in range(length) :
        val += random.choice(validChars)
    
    return val