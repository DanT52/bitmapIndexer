# bitmap_indexer.py

# output file format: inputFile_<sorted>_<compression>_<wordSize>


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
    output_file_name = output_path + "\\" + input_file.split("\\")[-1] + file_name_suffix

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
    pass
    """
    Compresses a bitmap index using the specified method and word size.

    :param bitmap_index: The path to the bitmap index file to be compressed.
    :param output_path: The path to where the compressed bitmap index should be written.
    :param compression_method: The compression method to use (e.g., "WAH").
    :param word_size: The word size to be used for compression.
    """
    # Your code here to read the bitmap index, compress it according to

    # the specified method and word size, and write the compressed data

    # to the output_path.



# Additional functions as needed for sorting data, compressing with WAH, etc.


create_index(r'testFiles\data\animals_small.txt', r'testFiles\my_outputs', False)