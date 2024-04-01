from bitmap_indexer import *

def cmp_files(file1, file2):
    with open(file1, "r") as f1:
        content1 = f1.readlines()
    with open(file2, "r") as f2:
        content2 = f2.readlines() 
    return content1 == content2

def test_bbc_8():
    compress_index("./output/bitmaps/animals.txt","./output/compressed","BBC",8)
    if cmp_files("./mine/compressed/animals_BBC_8", "./output/compressed/animals.txt_BBC_8"):
        print("Test BBC 8 Passed")
    else:
        print("Test BBC 8 Failed")

def test_bbc_8_small():
    compress_index("./output/bitmaps/animals_small.txt","./output/compressed","BBC",8)
    if cmp_files("./data/compressed/animals_small_BBC_8", "./output/compressed/animals_small.txt_BBC_8"):
        print("Test BBC 8 Small Passed")
    else:
        print("Test BBC 8 Small Failed")

def test_bbc_8_sorted():
    compress_index("./output/bitmaps/animals_sorted.txt_sorted","./output/compressed","BBC",8)
    if cmp_files("./mine/compressed/animalsSorted_sorted_BBC_8", "./output/compressed/animals_sorted.txt_sorted_BBC_8"):
        print("Test BBC 8 Sorted Passed")
    else:
        print("Test BBC 8 Sorted Failed")

def test_wah_8_weird():
    compress_index("./weird_bitmap.txt","./weirdlycompressed","WAH",8)
# Run the tests
    
test_bbc_8()
test_bbc_8_small()
test_bbc_8_sorted()

