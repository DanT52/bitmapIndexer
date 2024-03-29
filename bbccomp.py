def compress_bbc_line(dataline):
    compressed_line = []
    
    num_of_runs = 0
    current_literals = []
    num_of_lits = 0
    isDirtyBit = False
    dirty_bit_position = None

    def flush_compression():
        nonlocal compressed_line, num_of_runs, current_literals, num_of_lits, isDirtyBit, dirty_bit_position
        ending_byte = ""
        header = ""

        if num_of_runs <7:
            pass
        elif num_of_runs >= 7 and num_of_runs < 127:
            pass
        elif num_of_runs >= 127 and num_of_runs < 32768:
            pass

        if isDirtyBit:
            header+= "1"
            header += bin(dirty_bit_position)[2:].zfill(4)
            compressed_line += header + ending_byte
            flush_compression()
            return

        else:
            header+= "0"
            header += bin(num_of_lits)[2:].zfill(4)

        

        

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
