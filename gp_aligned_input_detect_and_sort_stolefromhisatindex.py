#!/usr/bin/env python3


from io import StringIO
import os
import subprocess
from subprocess import PIPE, STDOUT
import sys

import pysam

# commandLine=perl /htseq_count/htseq_count_wrapper.pl --htseqcount htseq-count --input <input.files> <sample.names> --gtf <GTF.file> --strand <strandedness> --minqual <min.qual> --mode <mode> --nonunique <count.nonunique> --secondary <count.secondary> --supplementary <count.supplementary> --featuretype <feature.type> --idtype <id.type> <gene.name> --output <output.file> --outformat <output.format>

def generate_command():
    buff = StringIO()
    buff.write(u"htseq-count ")

    allargs = iter(sys.argv[1:])
    for arg in allargs:
        # NOTE need to return the array to use globally
        if (arg.startswith('--input'))
            # should be a file list
            val = next(allargs, None)
            buff.write(u" ")

            with open(val) as f:
                content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [alignfile.strip() for alignfile in content]

            # check to see if input appears to be intact & print files names that don't pass to stdout
            # !does not read the middle of the file! see samtools doc for more information
            print("running samtools quickcheck")
            for alignfile in content:
                try:
                    pysam.quickcheck("-v", alignfile)
                except:
                    print("One or more files is not intact. See below for more information")
                else:
                    print("quickcheck okay")

                # file extension check/format detection
                # This can be removed in a future version when
                # htseq-count no longer requires a parameter it is ignoring...
                print("determining file extension")
                exts = [os.path.splitext(alignfile)[1]]
                #file_extension = os.path.splitext(alignfile)[1]

                # check that all extensions are the same
                extensions = exts
                check = True

                for x in exts:
                    if extensions != x:
                        check = False
                        break

                    if check:
                        print("All extensions are the same")
                        file_extension = x
                        print("input is " + file_extension)
                        return file_extension

                    else:
                        print("Files are not of the same format")
                        return



                # samtools sort [-l level] [-m maxMem] [-o out.bam] [-O format]
                # [-n] [-t tag] [-T tmpprefix] [-@ threads] [in.sam|in.bam|in.cram]
                sorted_input = pysam.sort(
                    "-o",
                    alignfile + "_nameSort" + file_extension,
                    "-n",
                    alignfile)
                print('sorted')
                print("sorted file name is " + alignfile + "_nameSort" + file_extension)

                return file_extension


            # need to check that the file extensions match ==
            # need to write the sorted files back into the expected GP file list


# get the original command line
orig_cmd = str(sys.argv[1:])
print("Original command line was " + orig_cmd)
# Make new command line with sorted_input
# & file_extension converted to the default value for format on the new command line.
# new_cmd =
# run htseq-count via original VIB perl wrapper with sorted file from this wrapper and format preset
# WHAT IS HAPPENING??
htseq_call = subprocess.Popen(["perl", "htseq_count_wrapper.pl", "--htseqcount htseq-count"], stdout=sys.stdout)
htseq_call.communicate()

# TO DO
# add file_extension to the other wrapper as the format variable
# sys.argv start at arg1 (not arg0) (or args.append? or parser.add.argument? - see opencravat)
