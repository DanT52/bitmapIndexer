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


"""
Compressesa bitmap index from a given index.
:param bitmap_index: The path to the bitmap index file.
:param output_path: The path to where the compressed bitmap index should be written.
:compression_method: The compression method to use.
:word_size: The word size to use for the compression.
"""
def compress_index(bitmap_index, output_path, compression_method, word_size):
    if compression_method != "WAH" and compression_method != "BBC":
        raise ValueError("Unsupported compression method: {}".format(compression_method))
    
    # Set the word size to 8 if the compression method is BBC
    if compression_method == "BBC":
        word_size = 8

    # Generate the output file name
    input_file_name = os.path.basename(bitmap_index)
    output_file_name = f"{input_file_name}_{compression_method}_{word_size}"
    output_file_path = os.path.join(output_path, output_file_name)

    # Create the directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Import the bitmap data
    bitmap_data = import_bitmap(bitmap_index)

    # Compress the bitmap data
    with open(output_file_path, 'w') as output_file:
        for line in bitmap_data:
            compressed_line = compress_wah_line(line, word_size) if compression_method == "WAH" else compress_bbc_line(line)
            output_file.write(compressed_line + '\n')



    

"""
Imports a bitmap from a file.
:param file_path: The path to the file containing the bitmap.
:returns: The imported transposed bitmap as a list of lists.
"""
def import_bitmap(file_path):
    with open(file_path, 'r') as f:
        #get each line and rm \n
        data = [list(line.strip()) for line in f]

    data_transposed = list(map(list, zip(*data)))

    return data_transposed



"""
Compresses a bitmap using the BBC compression method.
:param dataline: The bitmap line to compress.
:returns: The compressed bitmap line.
"""
def compress_bbc_line(dataline):
    compressed_line = ""
    num_of_runs = 0
    current_literals = []
    num_of_lits = 0

    #flush the current compression state
    def flush_compression(padded=False):
        nonlocal compressed_line, num_of_runs, current_literals, num_of_lits
        ending_byte = ""
        header = ""

        #determine the header
        if num_of_runs == 0:
            header+= "000"
        elif num_of_runs <7:
            header +=  bin(num_of_runs)[2:].zfill(3)
        elif num_of_runs >= 7 and num_of_runs < 127:
            header+= "111"
            ending_byte += "0" + bin(num_of_runs)[2:].zfill(7) #7 bits
        elif num_of_runs >= 127 and num_of_runs < 32768:
            header+= "111"
            ending_byte += "1" + bin(num_of_runs)[2:].zfill(15) #15 bits

        #determine if the current literal should be encoded as a dirty bit
        if num_of_lits == 1 and current_literals[0].count('1') == 1 and not padded:
            header += "1"
            header += bin(current_literals[0].find('1'))[2:].zfill(4)
            compressed_line += header + ending_byte
        else: #encode the literals
            header+= "0"
            header += bin(num_of_lits)[2:].zfill(4)
            compressed_line += header + ending_byte + ''.join(current_literals) 

        #reset the compression state
        num_of_runs = 0
        num_of_lits = 0
        current_literals = []

        
    index = 0
    while ((index+8) <= len(dataline)): #iterate over the bitmap line

        segment = dataline[index:index+8] #get the current segment

        if len(set(segment)) == 1 and segment[0]=="0": #check if the segment is a run
            if current_literals: #flush if there is already literals in the current state
                flush_compression()
            num_of_runs += 1

        else: #add the segment to the literals
            num_of_lits += 1
            current_literals.append(''.join(segment))
        if num_of_lits == 15: #flush if the literals are 15 (max literals that can be encoded in a chunk)
            flush_compression()
        if num_of_runs == 32767: #flush if the runs are 32767 (max runs that can be encoded in a chunk)
            flush_compression()
        
        index += 8

    #flush the remaining bits
    remaining_bits = dataline[index:]

    if remaining_bits:
        current_literals += ''.join(remaining_bits).ljust(8, '0') #pad the remaining bits
        num_of_lits += 1
    
    if current_literals or num_of_runs > 0:
        flush_compression(padded=True) if remaining_bits else flush_compression()
    

    return compressed_line



"""
Compresses a bitmap using the WAH compression method.
:param dataline: The bitmap line to compress.
:param word_size: The word size to use for the compression.
:returns: The compressed bitmap line.
"""
def compress_wah_line(dataline, word_size):
    compressed_line = ""
    index = 0
    runs = 0
    run_type = None
    literal_len = word_size - 1

    #save the current run state
    def save_run(run_bit, num_of_runs):
        nonlocal compressed_line
        compressed_line += '1' + run_bit + format(num_of_runs, 'b').zfill(literal_len - 1)

    #save the current literal
    def save_literal(literal):
        nonlocal compressed_line
        compressed_line += '0' + literal

    
    while ((index+literal_len) <= len(dataline)):

        segment = dataline[index:index+literal_len] #get the current segment

        if runs == 2**(literal_len - 1) - 1: #check if the runs are at the max
            save_run(run_bit, runs)
            runs = 0
            run_type = None

        if len(set(segment)) == 1: #check if the segment is a run
            run_bit = segment[0]

            if runs == 0: #start a new run
                run_type = run_bit
                runs += 1

            elif segment[0] == run_type: #continue the run
                runs += 1

            else:
                save_run(run_type, runs) #save the current run
                run_type = run_bit
                runs = 1
        else:                           #add the segment to the literals
            if runs > 0:
                save_run(run_type, runs)
                runs = 0
                run_type = None

            save_literal(''.join(segment))

        index += literal_len
    
    if runs > 0: #save the remaining runs
        save_run(run_type, runs)
        runs = 0
        run_type = None
    
    remaining_bits = dataline[index:] #get the remaining bits

    if remaining_bits: #save
        save_literal(''.join(remaining_bits).ljust(literal_len, '0'))

    return compressed_line

