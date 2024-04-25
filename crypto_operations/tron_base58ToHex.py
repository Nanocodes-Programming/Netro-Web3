import base58
import binascii

def base58_to_hex(base58_str):
    # Decode the Base58 string to bytes
    bytes_data = base58.b58decode(base58_str)
    
    # Remove the leading zero byte (if present) added during Base58 encoding
    leading_zeros = len(base58_str) - len(base58_str.lstrip('1'))
    hex_data = bytes_data[leading_zeros:] if leading_zeros > 0 else bytes_data

    # Convert bytes to hexadecimal
    hex_str = binascii.hexlify(hex_data).decode('utf-8')

    return hex_str[0:-8]


