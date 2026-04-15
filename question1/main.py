def get_file_data(path):    # Reads the content of a file and returns it as a string
    f = open(path)
    data = f.read()
    f.close()
    return data


# Generates a cipher mapping for characters in the range from start to end with a given shift
def gen_cipher(start, end, shift):
    diff = ord(end)-ord(start)+1
    cipher = {chr(value+ord(start)): chr(((value+shift) % diff)+ord(start))
              for value in range(diff)}
    return cipher


# Transforms the text using the provided mapping and leaves characters unchanged if they are not in the mapping.
def transform(text, mapping):
    return ''.join(map(lambda x: mapping[x] if x in mapping else x, text))


# Reads input file, generates ciphers, encrpyts the data using the ciphers, and writes the encrypted data to the output file.
def encrypt(ip, op, shift1, shift2):
    data = get_file_data(ip)    # Getting data to encrypt from input file path

    # Generating ciphers for differenct character ranges based on the provided shift values.
    a_m_cipher = gen_cipher('a', 'm', shift1 * shift2)
    n_z_cipher = gen_cipher('n', 'z', -(shift1 + shift2))
    A_M_cipher = gen_cipher('A', 'M', -shift1)
    N_Z_cipher = gen_cipher('N', 'Z', shift2**2)

    # Combining all the generated ciphers into a single mapping for encryption.
    cipher = {**a_m_cipher, **n_z_cipher, **A_M_cipher, **N_Z_cipher}

    encrypted_data = transform(data, cipher)
    with open(op, 'w') as file:
        file.write(encrypted_data)

    return cipher   # Returning the cipher used for decryption purposed later on


# Reads encrypted file, reverses the cipher mapping, decrypts the data, and writes the decrypted data to the output file.
def decrypt(ip, op, cipher):
    data = get_file_data(ip)    # Getting encrypted data from input file path
    # Reversing the cipher to restore original character mappings
    rev_cipher = {v: k for k, v in cipher.items()}
    decrypted_data = transform(data, rev_cipher)
    with open(op, 'w') as file:
        file.write(decrypted_data)


# Reads two files and checks whether their contents match to verify decryption was successful.
def verify(path1, path2):
    file1 = get_file_data(path1)    # Getting data from the original file
    file2 = get_file_data(path2)    # Getting data from the decrypted file
    if file1 == file2:
        print('The decryption is successful.')
    else:
        print('The decryption is not successful')


def get_input():    # Prompts the user to enter two shift values and validates the input to ensure they are integers.
    shifts = []
    while len(shifts) < 2:  # Loop until two shift values are entered
        try:
            shift = int(input(f'Enter shift {len(shifts)+1}: '))
            shifts.append(shift)
        except ValueError:
            print('Invalid input. Please enter an integer value.')
    return shifts[0], shifts[1]


def main():
    shift1, shift2 = get_input()
    try:    # Handle any exceptions that may occur.
        cipher = encrypt('raw_text.txt', 'encrypted_text.txt', shift1, shift2)    # Encrypt the text using the provided shift values.
        decrypt('encrypted_text.txt', 'decrypted_text.txt', cipher)    # Decrypt the text using the provided cipher.
        verify('raw_text.txt', 'decrypted_text.txt')    # Verify the decrypted text matches the original text.
    except Exception as e:
        print(f'An error occurred: {e}')    # Print the error message if an exception occurs.
        return


if __name__ == '__main__':
    main()
