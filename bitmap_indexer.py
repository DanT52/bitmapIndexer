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
    
    
    
    
    
    def read_bitmap(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    
    def write_compressed(compressed_data, file_path):
        with open(file_path, 'w') as file:
            file.write('\n'.join(compressed_data))
    
    def wah_compress(bitmap, word_size):
        # Adjust for control bit
        literal_len = word_size - 1
        compressed_data = []
        current_fill = None
        fill_len = 0
        
        for i in range(0, len(bitmap), literal_len):
            segment = bitmap[i:i + literal_len]
            
            # Check if segment can form a fill
            if segment == '0' * len(segment) or segment == '1' * len(segment):
                fill_bit = segment[0]
                if current_fill == fill_bit:
                    fill_len += 1
                else:
                    if current_fill is not None:
                        # Write previous fill
                        compressed_data.append('1' + current_fill + format(fill_len, f'0{literal_len - 1}b'))
                    current_fill = fill_bit
                    fill_len = 1
            else:
                # Write any pending fill before a literal
                if current_fill is not None:
                    compressed_data.append('1' + current_fill + format(fill_len, f'0{literal_len - 1}b'))
                    current_fill = None
                    fill_len = 0
                compressed_data.append('0' + segment)
        
        # Handle remaining fill
        if current_fill is not None:
            compressed_data.append('1' + current_fill + format(fill_len, f'0{literal_len - 1}b'))
        
        return compressed_data
    
    
 


    # with open(bitmap_index, 'r') as f:
    #     data = np.array([list(line.strip()) for line in f])
    # data_transposed = data.transpose()




    
    data = import_bitmap(bitmap_index)
    compressed_data_line = compress_wah_line(data[0], word_size)
    print(compressed_data_line)

    

    #compressed_data = wah_compress(bitmap, word_size)
    #write_compressed(compressed_data, output_path)
    

def import_bitmap(file_path):
    with open(file_path, 'r') as f:
        data = [list(line.strip()) for line in f]

    data_transposed = list(map(list, zip(*data)))

    return data_transposed


def compress_wah_line(dataline, word_size):
    compressed_line = ""
    index = 0
    literal_len = word_size - 1

    def save_run(run_bit, num_of_runs):
        compressed_line += '1' + run_bit + format(num_of_runs, 'b').zfill(literal_len - 1)
    def save_literal(literal):
        compressed_line += '0' + literal
    
    while index < len(dataline):
        segment = dataline[index:index+literal_len]

        #save current run state
        runs = 0
        run_type = None
        if runs == 2**(literal_len - 1):
            save_run(run_bit, run_length)
            runs = 0
            run_type = None

        if len(set(segment)) == 1:
            # The segment is a run
            run_bit = segment[0]
            run_length = 1

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




            while index + run_length < len(dataline) and dataline[index + run_length] == run_bit:
                run_length += 1
                if run_length == 2**(literal_len - 1):
                    save_run(run_bit, run_length)
                    index += run_length
                    run_length = 0
            if run_length > 0:
                save_run(run_bit, run_length)
                index += run_length
        else:
            # The segment is a literal
            literal = ''.join(segment)
            save_literal(literal)
            index += literal_len


    while index < len(dataline):
        segment = dataline[index:index+literal_len]

        # Check if the segment is a run
        if len(set(segment)) == 1:
            # The segment is a run
            run_bit = segment[0]
            run_length = 1
            while index + run_length < len(dataline) and dataline[index + run_length] == run_bit:
                run_length += 1
                if run_length == 2**(literal_len - 1):
                    compressed_line += '1' + run_bit + format(run_length, 'b').zfill(literal_len - 1)
                    index += run_length
                    run_length = 0
            if run_length > 0:
                compressed_line += '1' + run_bit + format(run_length, 'b').zfill(literal_len - 1)
                index += run_length
        else:
            # The segment is a literal
            literal = '0' + ''.join(segment)
            compressed_line += literal
            index += literal_len

    # Handle the remaining bits
    remaining_bits = dataline[index:]
    if remaining_bits:
        if len(set(remaining_bits)) == 1:
            # The remaining bits are a run
            compressed_line += '1' + remaining_bits[0] + format(len(remaining_bits), 'b').zfill(literal_len - 1)
        else:
            # The remaining bits are a literal
            literal = '0' + ''.join(remaining_bits) + '0' * (literal_len - len(remaining_bits))
            compressed_line += literal

    return compressed_line



    

# Additional functions as needed for sorting data, compressing with WAH, etc.


#create_index(r"testFiles\data\animals_small.txt", r"testFiles\my_outputs", False)
compress_index(r"testFiles/data/bitmaps/animals_small", r"testFiles\my_outputs\compressed", "WAH", 8)