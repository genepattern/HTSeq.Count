#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

import pysam

parser = argparse.ArgumentParser()
parser.add_argument("-", "--input",
                    dest="alignment_file",
                    default=None,
                    type=str,
                    help="Input file(s) in SAM or BAM format.")
args = parser.parse_args()

# # !! need to make these all in a for loop - can have more than 1 input file
# https://docs.python.org/3/library/fileinput.html#module-fileinput

# check to see if input appears to be intact & print files names that don't pass to stdout
# !does not read the middle of the file! see samtools doc for more information
print("running samtools quickcheck")
pysam.quickcheck("-v", args.alignment_file)
print("quickcheck okay")

# file extension check/format detection
# This can be removed in a future version when 
# htseq-count no longer requires a parameter it is ignoring...
print("determining file extension")
filename, file_extension = os.path.splitext(args.alignment_file)
# print("input file basename is " + filename)
print("input is " + file_extension)


# samtools sort [-l level] [-m maxMem] [-o out.bam] [-O format]
# [-n] [-t tag] [-T tmpprefix] [-@ threads] [in.sam|in.bam|in.cram]
sorted_input = pysam.sort(
    "-o",
    args.alignment_file + "_nameSort" + file_extension,
    "-n",
    args.alignment_file)
print('sorted')
print("sorted file name is " + args.alignment_file + "_nameSort" + file_extension)


# get the original command line
orig_cmd = str(sys.argv[1:])
print("Original command line was " + orig_cmd)
# Make new command line with sorted_input
# & file_extension converted to the default value for format on the new command line.

# run htseq-count via original VIB perl wrapper with sorted file from this wrapper and format preset
# WHAT IS HAPPENING??
htseq_call = subprocess.Popen(["perl", "htseq_count_wrapper.pl", sorted_input], stdout=sys.stdout)
htseq_call.communicate()

# TO DO
# add file_extension to the other wrapper as the format variable
# need to pass values to htseq_count_wrapper - rebuild command line? - better if you concat orig 
# sys.argv start at arg1 (not arg0) (or args.append? or parser.add.argument? - see opencravat)
