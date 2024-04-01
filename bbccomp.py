def compress_bbc_line(dataline):
    compressed_line = []
    
    num_of_runs = 0
    current_literals = []
    num_of_lits = 0


    def flush_compression():
        nonlocal compressed_line, num_of_runs, current_literals, num_of_lits
        ending_byte = ""
        header = ""

        if num_of_runs == 0:
            header+= "000"
        elif num_of_runs <7:
            header+= "111"
        elif num_of_runs >= 7 and num_of_runs < 127:
            header+= "111"
        elif num_of_runs >= 127 and num_of_runs < 32768:
            header+= "111"

        if num_of_lits == 1 and current_literals[0].find('1') != -1:
            header += "1"
            header += bin(current_literals[0].find('1'))[2:].zfill(4)
            compressed_line += header + ending_byte
        else:
            header+= "0"
            header += bin(num_of_lits)[2:].zfill(4)
            compressed_line += header + ''.join(current_literals) + ending_byte

        num_of_runs = 0
        num_of_lits = 0
        current_literals = []

        
    index = 0
    while ((index+8) <= len(dataline)):

        segment = dataline[index:index+8]

        if len(set(segment)) == 1 and segment[0]=="0":
            if current_literals:
                flush_compression()
            num_of_runs += 1

        else:
            num_of_lits += 1
            current_literals.append(''.join(segment))
        if num_of_lits == 15:
            flush_compression()
        if num_of_runs == 32767:
            flush_compression()
    
    remaining_bits = dataline[index:]
    return compressed_line


    # Convert to binary string representation for easier verification
    compressed_line_binary = ' '.join([f'{byte:08b}' for byte in compressed_line])
    return compressed_line_binary

# Test Cases
dataline_432_zeros_3_literals = ['0','0','0','0','0','0','0','0',] * 432 + ['1','0','1','0','1','0','1','0'] * 3
expected_output_432_zeros_3_literals = "11100011 10000001 10110000 10101010 10101010 10101010"

# compressed_line_432_zeros_3_literals = compress_bbc_line(dataline_432_zeros_3_literals)

# print("Compressed Line:", compressed_line_432_zeros_3_literals)
# print("Matches Expected:", compressed_line_432_zeros_3_literals == expected_output_432_zeros_3_literals)

def print_file_8_chars_at_a_time(file_path, occurrence):
    with open(file_path, 'r') as file:
        line_count = 0
        skip_count = 0
        header = False
        count_after_0001 = 0
        stop_after = 5
        found_0001 = 0
        while True:
            header = False

            chars = file.read(8)
            if not chars or (found_0001 == occurrence and count_after_0001 >= stop_after):
                break

            if skip_count == 0:
                print("# ", end='')
                header = True
            if skip_count == 0 and chars[3] == '0':
                skip_count = int(chars[4:], 2)
                print(skip_count)

            if chars.startswith('0001') and header:
                print(chars + ' ****')
                found_0001 += 1
            elif skip_count > 0 and not header:
                print(chars + ' !')
                skip_count -= 1
            else:
                print(chars)

            if found_0001 == occurrence:
                count_after_0001 += 1

            line_count += 1

print_file_8_chars_at_a_time("mine/compressed/animals_BBC_8", 6)

