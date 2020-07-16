#!/usr/bin/env python3

import os
import pysam

input_filename = 

# check to see if input appears to be intact & print files names that don't pass to stdout
# !does not read the middle of the file!
# see samtools doc for more information
pysam.quickcheck("-v", "manifest")
print('quickchecked')

# file extenstion check/format detection
# This can be removed in a future version when htSeq-count no longer requires a paramter it is ignoring...
filename, file_extension = os.path.splitext('/path/to/somefile.ext')
print(filename)
print(file_extension)
#send file_extension to the other wrapper.

pysam.sort("-o", "SRR1039508.mapped.Pos_sorted.bam", "-n", "SRR1039508.mapped.Pos_sorted.bam")
print('sorted')

# TO DO
# 7.15.20 - need variables for input.filename & out - set these at the top and reuse throughout
# need to pass values to htseq_count_wrapper