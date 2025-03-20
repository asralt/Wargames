import base64
import json
import urllib.parse  # For URL decoding

def xor_encrypt_decrypt(input_text, key):
    """ XOR encrypts or decrypts the input_text using the key """
    return bytes([input_text[i] ^ key[i % len(key)] for i in range(len(input_text))])

# The known plaintext (original JSON before encryption)
plaintext = json.dumps({"showpassword": "no", "bgcolor": "#ffffff"}).encode()

# The encrypted base64 cookie value (grab this from your browser)
encoded_cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GARUuXXNmTRg%3D"

# Fix URL-encoded characters
encoded_cookie = urllib.parse.unquote(encoded_cookie)  # Convert %3D back to '='

# Decode from Base64
decoded_cookie = base64.b64decode(encoded_cookie)

# Find the XOR key by XORing the known plaintext with the decoded cookie
key = xor_encrypt_decrypt(decoded_cookie, plaintext)
key = key[:4]  # Extract the repeating key

print(f"Extracted Key: {key.decode()}")  # Convert to string for display

# Now, modify the data to show the password
modified_data = json.dumps({"showpassword": "yes", "bgcolor": "#ffffff"}).encode()

# Encrypt using the extracted key
encrypted_modified = xor_encrypt_decrypt(modified_data, key)

# Encode to base64
new_cookie = base64.b64encode(encrypted_modified).decode()

print(f"Modified Cookie: {new_cookie}")

# Use this new cookie in your browser's console:
# document.cookie = "data=<new_cookie_value>";
