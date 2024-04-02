import os
from bitmap_indexer import compress_index  # Ensure this matches your actual import
import csv

# Define the configurations based on your pytest unit tests
configurations = [
    ("./output/bitmaps/animals.txt", "BBC", 8),
    ("./output/bitmaps/animals_small.txt", "BBC", 8),
    ("./output/bitmaps/animals_sorted.txt_sorted", "BBC", 8),
    ("./output/bitmaps/animals_small.txt", "WAH", 8),
    ("./output/bitmaps/animals_small.txt", "WAH", 16),
    ("./output/bitmaps/animals_small.txt", "WAH", 32),
    ("./output/bitmaps/animals_small.txt", "WAH", 64),
    ("./output/bitmaps/animals.txt", "WAH", 4),
    ("./output/bitmaps/animals.txt", "WAH", 8),
    ("./output/bitmaps/animals.txt", "WAH", 16),
    ("./output/bitmaps/animals.txt", "WAH", 32),
    ("./output/bitmaps/animals.txt", "WAH", 64),
    ("./output/bitmaps/animals_sorted.txt_sorted", "WAH", 4),
    ("./output/bitmaps/animals_sorted.txt_sorted", "WAH", 8),
    ("./output/bitmaps/animals_sorted.txt_sorted", "WAH", 16),
    ("./output/bitmaps/animals_sorted.txt_sorted", "WAH", 32),
    ("./output/bitmaps/animals_sorted.txt_sorted", "WAH", 64),
]

def run_compression_and_collect_stats(configurations):
    stats = []
    for file_path, compression_method, word_size in configurations:
        # Adjust the output path as needed
        output_path = "./output/compressed"
        # Ensure your compress_index function is updated to return total_fill_words and total_literals
        total_fill_words, total_literals = compress_index(file_path, output_path, compression_method, word_size)
        
        # # Calculate compressed file size
        # output_file_name = os.path.basename(file_path).replace(".txt", f"_{compression_method}_{word_size}")
        # compressed_file_path = os.path.join(output_path, output_file_name)
        # compressed_size_bytes = os.path.getsize(compressed_file_path)

        input_file_name = os.path.basename(file_path)
        output_file_name = f"{input_file_name}_{compression_method}_{word_size}"
        output_file_path = os.path.join(output_path, output_file_name)
        compressed_size_bytes = os.path.getsize(output_file_path)
        
        stats.append({
            "file_path": output_file_name,
            "compression_method": compression_method,
            "word_size": word_size,
            "total_fill_words": total_fill_words,
            "total_literals": total_literals,
            "compressed_size_bytes": compressed_size_bytes,
        })

    # Write stats to a CSV file
    with open('compression_stats.csv', 'w', newline='') as csvfile:
        fieldnames = ['file_path', 'compression_method', 'word_size', 'total_fill_words', 'total_literals', 'compressed_size_bytes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for stat in stats:
            writer.writerow(stat)

import os

def get_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        return size
    except OSError as e:
        print(f"An error occurred while getting the size of the file: {file_path}")
        print(f"Error details: {str(e)}")
        return None
    
if __name__ == "__main__":
    #run_compression_and_collect_stats(configurations)
    print(get_file_size("./data/bitmaps/animals"))
    print(get_file_size("./data/bitmaps/animals_small"))
    print(get_file_size("./data/bitmaps/animals_sorted"))
