import string
import secrets

# Initial Permutation Table
INIT_PERM = [58, 50, 42, 34, 26, 18, 10, 2,
				60, 52, 44, 36, 28, 20, 12, 4,
				62, 54, 46, 38, 30, 22, 14, 6,
				64, 56, 48, 40, 32, 24, 16, 8,
				57, 49, 41, 33, 25, 17, 9, 1,
				59, 51, 43, 35, 27, 19, 11, 3,
				61, 53, 45, 37, 29, 21, 13, 5,
				63, 55, 47, 39, 31, 23, 15, 7]
# Permuted Choice 1 table
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]
# Permuted choice 2 table
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Shifts for key schedule each round
SHIFT_SCHED = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Expansion permutation from 32-bit R half to 48-bit
EXP_PERM = [32, 1, 2, 3, 4, 5, 4, 5,
		6, 7, 8, 9, 8, 9, 10, 11,
		12, 13, 12, 13, 14, 15, 16, 17,
		16, 17, 18, 19, 20, 21, 20, 21,
		22, 23, 24, 25, 24, 25, 26, 27,
		28, 29, 28, 29, 30, 31, 32, 1]

# S-box tables
S_BOX = [
    # S-box 1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S-box 2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S-box 3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S-box 4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S-box 5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S-box 6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S-box 7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S-box 8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]
# Permutation function(P) table
PERM_FUNC = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]
# Inverse permutation table
INV_PERM = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# 64 bit ascii to binary
def ascii_to_bin(input_str):
    binary_str = ''.join(format(ord(i),'08b') for i in input_str)
    binary_str = binary_str[:64].ljust(64,'0')
    return binary_str 

# 64 bit binary to ascii
def bin_to_ascii(binary):
    str_out = ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])
    return str_out

# Function for permutation between block and predefined table
def permute(block, table):
    return [block[i-1] for i in table]

# Perform xor operation
def xor(a, b):
    return [str(int(ai) ^ int(bi)) for ai, bi in zip(a,b)]

# Round key generation
def round_key_gen(key):
    bin_key = ascii_to_bin(key)
    # Reduce 64-bit key into 56-bit
    pc1_key = permute(bin_key, PC1)

    # Split 56-bit key into two 28-bit
    left = pc1_key[:28]
    right = pc1_key[28:]
    round_keys = []
    for round_num in range(16):
        # Perform left circular shift on left and right
        left = left[SHIFT_SCHED[round_num]:] + right[:SHIFT_SCHED[round_num]]
        right = right[SHIFT_SCHED[round_num]:] + left[:SHIFT_SCHED[round_num]]
        # Concatenate left and right 
        tmp_key = left + right

        # Apply PC2 permutation
        pc2_key = permute(tmp_key, PC2)

        # Store the round key
        round_keys.append(pc2_key)
        
    return round_keys

# DES Encryption
def des_encrypt(str_input, encrypt_key):
    bin_input = ascii_to_bin(str_input)
    round_keys = round_key_gen(ascii_to_bin(encrypt_key))
    
    init_perm_input = permute(bin_input, INIT_PERM)
    
    lpt = init_perm_input[:32]
    rpt = init_perm_input[32:]
    
    # Assume 'rpt' is the 32-bit right half, 'lpt' is the 32-bit left half, and 'round_keys' is a list of 16 round keys
    for round_num in range(16):
        # Perform expansion (32 bits to 48 bits)
        expanded_perm_str = ''.join(permute(rpt, EXP_PERM))

        # Round key for the current round
        round_key_str = round_keys[round_num]

        # Perform xor operation
        xor_str = ''.join(xor(expanded_perm_str, round_key_str))
        
        # Split the 48-bit string into 8 groups of 6 bits each
        six_bit_groups = [xor_str[i:i+6] for i in range(0, 48, 6)]

        # Initialize the substituted bits string
        s_box_substituted = ''

        # Apply S-box substitution for each 6-bit group
        for i in range(8):
            # Extract the row and column bits
            row_bits = int(six_bit_groups[i][0] + six_bit_groups[i][-1], 2)
            col_bits = int(six_bit_groups[i][1:-1], 2)

            # Lookup the S-box value
            s_box_value = S_BOX[i][row_bits][col_bits]
            
            # Convert the S-box value to a 4-bit binary string and append to the result
            s_box_substituted += format(s_box_value, '04b')

        # Apply a P permutation function to the result
        p_box_result = ''.join(permute(s_box_substituted, PERM_FUNC))

        # Perform XOR operation
        new_rpt = xor(lpt, p_box_result)

        # Update LPT and RPT for the next round
        lpt = rpt
        rpt = new_rpt

    # After the final round, reverse the last swap
    final_result = rpt + lpt

    # Perform the final permutation (IP-1)
    final_cipher = ''.join(permute(final_result, INV_PERM))

    # Convert binary cipher to ascii
    final_cipher_ascii = bin_to_ascii(final_cipher)
    #print("Final Cipher text:", final_cipher_ascii , len(final_cipher_ascii))
    
    return final_cipher_ascii

# DES Decryption
def des_decrypt(final_cipher, encrypt_key):
    
    # Initialize lists to store round keys
    round_keys = round_key_gen(ascii_to_bin(encrypt_key))
    bin_cipher = ascii_to_bin(final_cipher)
    
    # Apply Initial Permutation
    ip_dec_result_str = ''.join(permute(bin_cipher, INIT_PERM))
    
    lpt = ip_dec_result_str[:32]
    rpt = ip_dec_result_str[32:]

    for round_num in range(16):
        # Perform expansion (32 bits to 48 bits)
        expanded_result = ''.join(permute(rpt, EXP_PERM))
        
        # Round key for the current round
        round_key_str = round_keys[15-round_num]
    
        # XOR between key and expanded result 
        xor_result_str = ''.join(xor(expanded_result, round_key_str))
        
        # Split the 48-bit string into 8 groups of 6 bits each
        six_bit_groups = [xor_result_str[i:i+6] for i in range(0, 48, 6)]
    
        # Initialize the substituted bits string
        s_box_substituted = ''
    
        # Apply S-box substitution for each 6-bit group
        for i in range(8):
            # Extract the row and column bits
            row_bits = int(six_bit_groups[i][0] + six_bit_groups[i][-1], 2)
            col_bits = int(six_bit_groups[i][1:-1], 2)
    
            # Lookup the S-box value
            s_box_value = S_BOX[i][row_bits][col_bits]
            
            # Convert the S-box value to a 4-bit binary string and append to the result
            s_box_substituted += format(s_box_value, '04b')
    
        # Apply a P permutation to the result
        p_box_result = ''.join(permute(s_box_substituted, PERM_FUNC))
    
        # Perform XOR operation
        new_rpt = xor(lpt, p_box_result)
    
        # Update LPT and RPT for the next round
        lpt = rpt
        rpt = new_rpt
    
    final_result = rpt + lpt
    
    # Perform the final inverse permutation (IP-1)
    final_cipher = ''.join(permute(final_result, INV_PERM))

    # binary cipher string to ascii
    final_cipher_ascii = bin_to_ascii(final_cipher)
    #print("Decryption of Cipher :", final_cipher_ascii)

    return final_cipher_ascii

# Split the string into 64-bit each
def split_str(input_str):
    return [input_str[i:i+8] for i in range(0, len(input_str), 8)]

# Batch encryption for larger input
def batch_encrypt(str_input, key):
    str_list = split_str(str_input)
    res_cipher = ''
    
    for i in str_list:
        res_cipher += des_encrypt(i, key)
    
    #print("Encrypt Result: ")
    #print(res_cipher)
    return res_cipher

# Batch decryption for larger input        
def batch_decrypt(cipher, key):
    str_list = split_str(cipher)
    res_str = ''
    
    for i in str_list:
        res_str += des_decrypt(i, key)

    #print("Decrypt Result: " + res_str)
    return res_str

def generate_key():
    alphabet = string.ascii_letters + string.digits
    keys = ''.join(secrets.choice(alphabet) for i in range(8))
    return keys

#keys = input("Enter encryption key (max 8 characters): ")
# print("DES Encryption and Decryption")
# print("1. Encryption\n2. Decryption\n3. Exit")
# x = input("Enter choice: ")
# if x == "1":
#     user_input = input("Enter message: \n")
#     keys = input("Enter key: \n")
#     #keys = generate_key()    
#     #print("Key generated: " + keys)
#     enc = batch_encrypt(user_input, keys)
#     dec = batch_decrypt(enc, keys)
# elif x == "2":
#     user_cipher = input("Enter cipher message: \n")
#     key = input("Enter cipher key: \n")
#     dec = batch_decrypt(user_cipher, keys)
# elif x == "3":
#     exit()

# user_input = input("Enter message: \n")
# keys = generate_key()

# print("Generated key used for DES: " + keys)

# enc = batch_encrypt(user_input, keys)
# dec = batch_decrypt(enc, keys)

#print(enc)
#enc = des_encrypt(user_input, keys)
#dec = des_decrypt(enc, keys)
#print(enc)