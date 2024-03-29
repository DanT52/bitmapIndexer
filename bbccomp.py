def compress_bbc_line(dataline):
    compressed_line = []
    
    current_run_length = 0
    current_literals = []

    def flush_compression():
        nonlocal compressed_line, current_run_length, current_literals
        header_byte = 0

        if current_run_length > 0:
            if current_run_length <= 6:
                # Encode run length in the header if <= 6
                header_byte = current_run_length
            elif 7 <= current_run_length <= 127:
                # For run lengths 7-127, set header to 111 and add a byte
                header_byte = 0b11100000
                compressed_line.append(header_byte)
                compressed_line.append(current_run_length)
            else:
                # For run lengths 128-32767, use two bytes
                header_byte = 0b11100000
                compressed_line.append(header_byte)
                compressed_line += [0b10000000 | (current_run_length >> 8), current_run_length & 0xFF]
            current_run_length = 0
        if current_literals:
            # Adjust the header for literals if not just flushing runs
            literals_len = len(current_literals)
            if literals_len <= 15:
                header_byte |= (literals_len << 4)
                compressed_line.insert(-len(current_literals)-1, header_byte)
            compressed_line += current_literals
            current_literals = []

    for index in range(0, len(dataline), 8):
        segment = dataline[index:index+8]

        if segment.count('0') == 8:
            if current_literals:
                flush_compression()
            current_run_length += 1
        elif segment.count('1') == 1:
            flush_compression()  # Ensure runs are flushed before handling a dirty bit
            # Handle single dirty bit
            dirty_bit_position = segment.find('1')
            compressed_line.append(0b10000000 | dirty_bit_position)
        else:
            # Literal handling
            current_literals.append(int(''.join(segment), 2))

    flush_compression()  # Ensure any remaining data is flushed

    # Convert to binary string representation for easier verification
    compressed_line_binary = ' '.join([f'{byte:08b}' for byte in compressed_line])
    return compressed_line_binary

# Test Cases
dataline_432_zeros_3_literals = ['0'] * 432 + ['10101010', '10101010', '10101010']
expected_output_432_zeros_3_literals = "11100011 10000001 10110000 10101010 10101010 10101010"

compressed_line_432_zeros_3_literals = compress_bbc_line(dataline_432_zeros_3_literals)

print("Compressed Line:", compressed_line_432_zeros_3_literals)
print("Matches Expected:", compressed_line_432_zeros_3_literals == expected_output_432_zeros_3_literals)
