# bitmap_indexer.py

# output file format: inputFile_<sorted>_<compression>_<wordSize>

import os

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
            return file.read().strip()
    
    def write_compressed(compressed_data, file_path):
        with open(file_path, 'w') as file:
            file.write(' '.join(compressed_data))
    
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
    
    bitmap = read_bitmap(bitmap_index)
    compressed_data = wah_compress(bitmap, word_size)
    write_compressed(compressed_data, output_path)


# Additional functions as needed for sorting data, compressing with WAH, etc.


#create_index(r"testFiles\data\animals_small.txt", r"testFiles\my_outputs", False)
compress_index(r"testFiles\data\bitmaps\animals_small", r"testFiles\my_outputs\compressed", "WAH", 32)