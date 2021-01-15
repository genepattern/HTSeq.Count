#!/usr/bin/env python3

from io import StringIO
import os
import subprocess
from subprocess import PIPE
import sys

import pysam


def generate_command():
    buff = StringIO()

    allargs = iter(sys.argv[1:])
    for arg in allargs:
        if arg.startswith('--input'):
            # should be a file list
            val = next(allargs, None)

            with open(val) as f:
                content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [alignfile.strip() for alignfile in content]
            print("content = " + str(content))

            # file extension check/format detection this can be removed in a future version when
            # htseq-count no longer requires a parameter it is ignoring...
            exts = []
            for alignfile in content:
                print("determining file extension")
                ext = os.path.splitext(alignfile)[1]
                # exts = [os.path.splitext(alignfile)[1]]
                # basename = os.path.splitext(alignfile)[0]
                print("The ext of " + alignfile + " is " + ext)
                exts.append(ext)
                print(exts)
                # return ext

            ele = exts[0]
            print(exts[0])

            # check that all extensions are the same
            check = True

            for x in exts:
                if ele != x:
                    check = False
                    print("Files are not of the same format")
                    break
                elif check:
                    global file_format
                    file_extension = exts[0]
                    file_format = file_extension.replace(".", "")
                    print("input format is " + file_format)

            buff.write(u"--format ")
            buff.write(file_format)
            print("All extensions are the same")

            # check to see if input appears to be intact & print files names that don't pass to stdout
            # !does not read the middle of the file! see samtools doc for more information
            for alignfile in content:
                print("running samtools quickcheck")
                print('alignfile = ' + alignfile)
                try:
                    pysam.quickcheck("-v", alignfile)
                except Exception:
                    print(alignfile + " is incorrectly formatted or truncated. See stderr for details.")
                    #raise ValueError(alignfile + ' is incorrectly formatted or truncated')
                    raise
                    #not sure that I need sys.exit here - given raise
                    #sys.exit(1)
                else:
                    print("quickcheck okay")

            sorted_alignfiles = []
            for alignfile in content:
                print("SORT DEBUG: content = " + str(content))
                # samtools sort [-l level] [-m maxMem] [-o out.bam] [-O format]
                # [-n] [-t tag] [-T tmpprefix] [-@ threads] [in.sam|in.bam|in.cram]
                #global sorted_input - don't think I need this now?
                try:
                    print("name sorting input")
                    print("SORT DEBUG: alignfile = " + alignfile)
                    tail = os.path.split(alignfile)[1]
                    # sorted_input = pysam.sort("-o", "_nameSort" + "." + file_format, "-n", alignfile)
                    pysam.sort(
                       "-o",
                       tail + "_nameSort" + "." + file_format,
                       "-n",
                       alignfile)
                except Exception:
                    print("There was an error sorting " + alignfile + " See stderr for details")
                    raise
                else:
                    print("sorted")
                    sorted_input = tail + "_nameSort" + "." + file_format
                    print("SORT DEBUG: sorted_input = " + sorted_input)
                    sorted_alignfiles.append(sorted_input)
                    print("SORT DEBUG: sorted_alignfiles = " + str(sorted_alignfiles))

            print("All sorted files = " + str(sorted_alignfiles))
            buff.write(u" --order name")
                #return sorted_alignfiles

                #all_inputs = [sorted_input]
                #print("These are all the sorted inputs " + str(all_inputs))
                #print("These are all the sorted inputs " + str(sorted_alignfiles))

                # write the sorted files back into the expected GP file list
                f = open("input.files.list", "w")
                for ele in sorted_alignfiles:
                    f.write(ele + '\n')
                f.close()

            return buff.getvalue()


# get the original command line
orig_cmd = str(sys.argv[1:])
print("Original command line was " + orig_cmd)

# Make new command line with sorted_input
# & file_extension converted to the default value for format on the new command line,
# using list comprehension
new_cmd = 'perl /htseq_count/htseq_count_wrapper.pl --htseqcount htseq-count --input input.files.list ' \
          + generate_command() + " " + ' '.join(map(str, sys.argv[5:]))
print("this is the new command: " + new_cmd)

childProcess = subprocess.Popen(new_cmd, shell=True, env=os.environ, stdout=PIPE, stderr=PIPE)
stdout, stderr = childProcess.communicate()
retval = childProcess.returncode
if retval != 0:
    # if non-zero return, print stderr to stderr
    print(stdout)
    print(stderr, file=sys.stderr)

# os.remove("input.files.list")
sys.exit(retval)
