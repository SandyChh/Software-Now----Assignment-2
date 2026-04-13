def get_file_data(path):    # Reads the content of a file and returns it as a string
    f = open(path)
    data = f.read()
    f.close()
    return data

def gen_cipher(start, end, shift):  # Generates a cipher mapping for characters in the range from start to end with a given shift
    diff = ord(end)-ord(start)+1
    cipher = {chr(value+ord(start)): chr(((value+shift)%diff)+ord(start)) for value in range(diff)}
    return cipher

def transform(text, mapping):   # Transforms the text using the provided mapping and leaves characters unchanged if they are not in the mapping.
    return ''.join(map(lambda x: mapping[x] if x in mapping else x, text))

def encrypt(ip, op, shift1, shift2):    # Reads input file, generates ciphers, encrpyts the data using the ciphers, and writes the encrypted data to the output file.
    data = get_file_data(ip)

    # Generating ciphers for differenct character ranges based on the provided shift values.
    a_m_cipher = gen_cipher('a', 'm', shift1 * shift2)
    n_z_cipher = gen_cipher('n', 'z', -(shift1 + shift2))
    A_M_cipher = gen_cipher('A', 'M', -shift1)
    N_Z_cipher = gen_cipher('N', 'Z', shift2**2)

    cipher = {**a_m_cipher, **n_z_cipher, **A_M_cipher, **N_Z_cipher}   # Combining all the generated ciphers into a single mapping for encryption.

    encrypted_data = transform(data, cipher)
    with open(op, 'w') as file:
        file.write(encrypted_data)
        
    return cipher   # Returning the cipher used for decryption purposed later on

def get_input():    # Prompts the user to enter two shift values and validates the input to ensure they are integers.
    shifts = []
    while len(shifts) < 2:
        try:
            shift = int(input(f'Enter shift {len(shifts)+1}: '))
            shifts.append(shift)
        except ValueError:
            print('Invalid input. Please enter an integer value.')
    return shifts[0], shifts[1]

def main():
    shift1, shift2 = get_input()
    try:    # Attempt to encrypt the text using the provided shift values and handle any exceptions that may occur during the process.
        cipher = encrypt('raw_text.txt', 'encrypted_text.txt', shift1, shift2)
    except Exception as e:
        print(f'An error occurred: {e}')
        return
    print(cipher)


if __name__ == '__main__':
    main()