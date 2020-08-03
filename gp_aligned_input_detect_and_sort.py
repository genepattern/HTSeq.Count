#!/usr/bin/env python3

import os
import pysam
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-", "--input", 
	                dest="alignment_file",
	                default = None,
                    type=str,
                    help="Input file(s) in SAM or BAM format.")
parser.parse_args()

# ~~~need to make this all a loop for all inputs provided~~
# main question is how to get the args off the command line - do I need to define that here? or does the argparse func above do that?
# probably don't need this
# parser.alignment_file =

# check to see if input appears to be intact 
# & print files names that don't pass to stdout
# !does not read the middle of the file!
# see samtools doc for more information
pysam.quickcheck("-v", parser.alignment_file)
print('quickchecked')

# file extension check/format detection
# This can be removed in a future version when 
# htseq-count no longer requires a parameter it is ignoring...
filename, file_extension = os.path.splitext(alignment_file)
print(filename)
print(file_extension)
#send file_extension to the other wrapper as the format variable

#samtools sort [-l level] [-m maxMem] [-o out.bam] [-O format] [-n] [-t tag] [-T tmpprefix] [-@ threads] [in.sam|in.bam|in.cram]
pysam.sort(
    "-o", 
    alignment_file + "_nameSort" + file_extension,
    "-n", 
    filename)
print('sorted')

# TO DO
# 7.15.20 - need variables for input.filename & out - set these at the top and reuse throughout
# need to pass values to htseq_count_wrapper - rebuild command line? - better if you concat orig 
# sys.argv start at arg1 (not arg0)
 