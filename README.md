## Prerequisites

- Python 3.x

## Usage
0. **Import the Module**

    ```python
    import bitmap_indexer
    ```
    If you only need specific functions from the module, you can import them directly using:

    ```python
    from bitmap_indexer import create_index, compress_index
    ```

1. **Create a Bitmap Index:**

   You can create a bitmap index from your data file by using the `create_index` function. This function requires three parameters:
   
   - `input_file`: The path to your input data file.
   - `output_path`: The directory where you want the bitmap index file to be saved.
   - `sorted`: A boolean indicating whether the data in your input file is sorted.
   
   Example command:
   ```python
   create_index('path/to/your/data.csv', 'path/to/output/directory', False)
   ```

2. **Compress a Bitmap Index:**

   Once you have a bitmap index, you can compress it using either the BBC or WAH compression methods with the `compress_index` function. This function requires four parameters:
   
   - `bitmap_index`: The path to the bitmap index file you want to compress.
   - `output_path`: The directory where you want the compressed bitmap index file to be saved.
   - `compression_method`: The compression method to use (`'WAH'` or `'BBC'`).
   - `word_size`: The word size to use for the compression (note: for BBC, the word size will automatically be set to 8).
   
   Example command:
   ```python
   compress_index('path/to/your/bitmap_index.txt', 'path/to/output/directory', 'WAH', 16)
   ```

## Note

- Ensure all paths provided are accessible and that the output directory exists or can be created by the script.
- The data file should be a CSV with columns for animal, age, and adopted status (in that order).

