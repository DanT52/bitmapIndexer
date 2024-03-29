# bitmap_indexer.py

# output file format: inputFile_<sorted>_<compression>_<wordSize>

import os
import numpy as np

"""
Creates a bitmap index from a data file.

:param input_file: The path to the input data file.
:param output_path: The path to where the bitmap index should be written.
:param sorted: Whether the data in the input file is sorted.
"""
def create_index(input_file, output_path, sorted):

    animals = ["cat", "dog", "turtle", "bird"] #list of possible animals

    #generate the output file name
    file_name_suffix = '_sorted' if sorted else ''
    base_name = os.path.basename(input_file)
    new_file_name = base_name + file_name_suffix
    output_file_name = os.path.join(output_path, new_file_name)

    # Create the directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    with open(input_file, 'r') as infile, open(output_file_name, 'w') as outfile:
        for line in infile:
            
            #get elements from row
            animal, age, adopted = line.strip().split(",")

            #animal bitmap
            bitmap_line = "".join(["1" if animal == a else "0" for a in animals])

            #determine age index
            index = (int(age) - 1) // 10
            #add age index to bitmap
            bitmap_line += "0" * index + "1" + "0" * (9 - index)

            #bitmap for true or false
            bitmap_line += "10" if adopted == "True" else "01"

            #write to outfile
            outfile.write(bitmap_line + '\n')



def compress_index(bitmap_index, output_path, compression_method, word_size):
    if compression_method != "WAH":
        raise ValueError("Unsupported compression method: {}".format(compression_method))
    
    input_file_name = os.path.basename(bitmap_index)
    output_file_name = f"{input_file_name}_{compression_method}_{word_size}"
    output_file_path = os.path.join(output_path, output_file_name)

    # Create the directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    bitmap_data = import_bitmap(bitmap_index)

    total_fill_words = 0
    total_literals = 0

    with open(output_file_path, 'w') as output_file:
        for line in bitmap_data:
            compressed_line, fill_words, literals = compress_wah_line(line, word_size)
            output_file.write(compressed_line + '\n')
            total_fill_words += fill_words
            total_literals += literals


    
    print(f"Done compressing {input_file_name}")
    print(f"Total fill words: {total_fill_words}")
    print(f"Total literals: {total_literals}")

    


    




def import_bitmap(file_path):
    with open(file_path, 'r') as f:
        #get each line and rm \n
        data = [list(line.strip()) for line in f]

    data_transposed = list(map(list, zip(*data)))

    return data_transposed


def compress_bbc_line(dataline):
    compressed_line = ""
    total_fill_words = 0
    total_literals = 0

    index = 0
    current_runs = 0
    current_literals = ""
    current_lit_count = 0
    dirty_bit_location = -1

    def flush_literals():
        nonlocal compressed_line, current_literals, current_lit_count, total_literals
        # Header for literals only, with the number of literals in bits 5-8
        if current_lit_count > 0:
            header = '1111' + format(current_lit_count, '04b')
            compressed_line += header + current_literals
            total_literals += current_lit_count
            current_literals = ""
            current_lit_count = 0

    def flush_runs():
        nonlocal compressed_line, current_runs, total_fill_words
        if current_runs == 0:
            return
        elif current_runs <= 6:
            # Encode directly in the header
            compressed_line += '111' + '0000' + format(current_runs - 1, '04b')
        elif current_runs <= 127:
            # One byte follows the header
            compressed_line += '111' + '0001' + format(current_runs, '08b')
        else:
            # Two bytes follow the header
            compressed_line += '111' + '0010' + format(current_runs, '016b')
        total_fill_words += current_runs
        current_runs = 0

    while ((index+8) <= len(dataline)):
        segment = dataline[index:index+8]
        index += 8

        if len(set(segment)) == 1 and segment[0] == '0':
            # Check if it's time to flush literals before adding more runs
            if current_lit_count > 0:
                flush_literals()
            current_runs += 1

        elif segment.count('1') == 1:
            location = segment.find('1')
            dirty_bit_location = 7 - location  # Adjusted for bit ordering in byte
            flush_runs()  # Flush runs before handling a dirty bit
            flush_literals()  # Make sure to flush literals as well
            # Handle single dirty bit case
            compressed_line += '1111' + format(dirty_bit_location, '04b') + segment
            total_literals += 1
        else:
            # Literal encountered
            if current_runs > 0:
                flush_runs()
            current_literals += segment
            current_lit_count += 1
            if current_lit_count == 15:
                flush_literals()

    # Flush remaining runs or literals after loop completion
    if current_runs > 0:
        flush_runs()
    if current_lit_count > 0:
        flush_literals()

    return compressed_line, total_fill_words, total_literals





def compress_wah_line(dataline, word_size):
    compressed_line = ""
    index = 0
    runs = 0
    run_type = None
    literal_len = word_size - 1
    fill_words = 0
    literals = 0

    def save_run(run_bit, num_of_runs):
        nonlocal compressed_line, fill_words
        compressed_line += '1' + run_bit + format(num_of_runs, 'b').zfill(literal_len - 1)
        fill_words += num_of_runs
    def save_literal(literal):
        nonlocal compressed_line, literals
        compressed_line += '0' + literal
        literals += 1
    
    while ((index+literal_len) <= len(dataline)):

        segment = dataline[index:index+literal_len]

        #save current run state

        if runs == 2**(literal_len - 1) - 1:
            save_run(run_bit, runs)
            runs = 0
            run_type = None

        if len(set(segment)) == 1:
            # The segment is a run
            run_bit = segment[0]

            if runs == 0:
                run_type = run_bit
                runs += 1

            elif segment[0] == run_type:
                runs += 1

            else:
                save_run(run_type, runs)
                run_type = run_bit
                runs = 1
        else:
            if runs > 0:
                save_run(run_type, runs)
                runs = 0
                run_type = None

            save_literal(''.join(segment))

        index += literal_len
    
    if runs > 0:
        save_run(run_type, runs)
        runs = 0
        run_type = None
    
    remaining_bits = dataline[index:]
    if remaining_bits:
        save_literal(''.join(remaining_bits).ljust(literal_len, '0'))

    return compressed_line, fill_words, literals



    
def print_differences(real, compressed):
    for i in range(0, len(real), 4):
        real_segment = real[i:i+4]
        compressed_segment = compressed[i:i+4]

        if real_segment == compressed_segment:
            print(real_segment)
            print(compressed_segment)
        else:
            print(real_segment, "*")
            print(compressed_segment, "*")
        print()

def print_first_difference(real, compressed, word_size):
    prev_real_segment = None
    prev_compressed_segment = None

    for i in range(0, len(real), word_size):
        real_segment = real[i:i+word_size]
        compressed_segment = compressed[i:i+word_size]

        if real_segment != compressed_segment:
            print(f"Difference found at position {i} to {i+word_size}, this is the {i//word_size}th segment")
            print("Real segment:", real_segment, "*")
            print("Compressed segment:", compressed_segment, "*")

            if prev_real_segment is not None:
                print("Previous real segment:", prev_real_segment, "*")
                print("Previous compressed segment:", prev_compressed_segment, "*")

            next_real_segment = real[i+word_size:i+2*word_size]
            next_compressed_segment = compressed[i+word_size:i+2*word_size]
            if next_real_segment and next_compressed_segment:
                print("Next real segment:", next_real_segment, "*")
                print("Next compressed segment:", next_compressed_segment, "*")

            break

        prev_real_segment = real_segment
        prev_compressed_segment = compressed_segment

# Additional functions as needed for sorting data, compressing with WAH, etc.


compress_index("./output/bitmaps/animals.txt","./output/compressed","WAH",4)
#create_index(r"testFiles\data\animals_small.txt", r"testFiles\my_outputs", False)
