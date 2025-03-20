import socket
import struct

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('vortex.labs.overthewire.org', 5842))

# Read exactly 16 bytes (4 unsigned integers, each 4 bytes)
data = b""
while len(data) < 16:
    chunk = s.recv(16 - len(data))  # Receive the remaining bytes
    if not chunk:
        print("Connection closed before receiving 16 bytes.")
        exit(1)
    data += chunk

# Unpack the received data as 4 little-endian unsigned integers
numbers = struct.unpack('<4I', data)  # '<' = little endian, 'I' = unsigned int

# Apply 32-bit integer overflow rule
total = sum(numbers) & 0xFFFFFFFF  # Ensure result is within 32-bit range

print(f"Numbers received: {numbers}")
print(f"Sum to send (32-bit wraparound): {total}")

# Send the sum as a 4-byte little-endian unsigned integer
s.send(struct.pack('<I', total))  # Pack it in little-endian format

# Receive response (should be username & password)
response = s.recv(1024)
print(f"Response: {response.decode()}")

# Close connection
s.close()
