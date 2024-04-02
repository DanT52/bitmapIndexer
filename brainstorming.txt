# bitmapIndexer

output file naming:

inputFile_<sorted>_<compression>_<wordSize>

wah compression:

start with beggining, work through each line:
loop through segments of length of the literal of each line.

if run then have a variable keep track that there is 1 run of "1" or "0"

if we run into a literal or a run of the other kind then we add to the compressed version.

if it is a literal then we like add code for the literal.

If the line has a set of bits at the end, then you may encode it as a literal and pad the rightmost side with 0s. A single
run of either 1’s or 0’s should be encoded as a run and not a literal.

for wah the first bit is telling us if the word is a run or literal, and the next bit lets us know if it is a run of "0" s or "1"s, the following buts are the number of runs, stored in binary

for a word size of 4 a run of "0"s that goes on for the length of 3 literals looks like:
1011



bbc compression:

Understanding the Header Byte
Bits 1-3: Indicate the number of runs if the size is between 0-6.
Bit 4: Indicates if the tail is special (e.g., a single literal byte with a specific bit set).
Bits 5-8: Indicate the number of literals at the end of the chunk or the location of the dirty bit in the special byte.
Storing Runs of Zeros
Runs of 0-6: Directly stored in the header byte.
Runs of 7-127: Require one additional byte following the header to count the gaps.
Runs of 128-32767: Require two additional bytes following the header to count the gaps.

A run of 13 bytes of 0's followed by two literals is like this 11100010 00001101

a run of 128 followed by 3 literals looks like 1110011 10000001 10110000

so i think my strategy for this function should be as follows

keep track of runs,

if we encounter a literal, we add it to current_literals and increment current lit count

if we encounter a run or a dirty bit, or the number of litererals reaches 15 we then have to add the current_literals to the compressed_line using the compression method.

if we are not in a run and encounter a dirty bit we use the compression method to store the dirty bit location

if we have counted a number of runs, and then get to some literals, we wait until we find another run, dirty bit, or the number of literals reaches 15 then we compress what we have gathered.


strat 2:

single flush

when to flush:

if literals followed by run:
    flush
    add run
if 15 literals:
    flush

if runs but no literals followed by dirty bit:
    flush

if no runs and literals followed by dirty bit:
    flush
    add ditry bit
    flush

if dirty bit and no runs and no literals:
    flush

if 32767 runs:
    flush

## strat 3:

So again i think we will still just keep track of:

#of runs
literals = []
num of literals =[]

this appraoch will just initially not care about dirty bits. we will just put them in the literals list with the other lits.

however in the flush function we will need to check if there is just one literal and it is a dirty bit, if that is the case then we will store it properly and use a special bit.

# when too flush:

if 15 literals:
    flush

if literals followed by run:
    flush

if runs and lits followed by run:
    flush
    
if 32767 runs:
    flush

    

