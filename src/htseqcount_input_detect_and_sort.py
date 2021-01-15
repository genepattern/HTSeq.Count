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
                print("The ext of " + alignfile + " is " + ext)
                exts.append(ext)

            ele = exts[0]
            # check that all extensions are the same
            check = True
            for x in exts:
                try:
                    if ele != x:
                        print("Alignment files are not of the same format")
                        check = False
                    elif check:
                        global file_format
                        file_extension = exts[0]
                        file_format = file_extension.replace(".", "")
                except Exception:
                    raise ValueError('Alignment files are not of the same format.')

            buff.write(u"--format ")
            buff.write(file_format)
            print("all extensions are the same")
            print("input format is " + file_format)

            # check to see if input appears to be intact & print files names that don't pass to stdout
            # !does not read the middle of the file! see samtools doc for more information
            for alignfile in content:
                print("running samtools quickcheck")
                print('alignfile = ' + alignfile)
                try:
                    pysam.quickcheck("-v", alignfile)
                except Exception:
                    print(alignfile + " is incorrectly formatted or truncated. See stderr for details.")
                    raise
                else:
                    print("quickcheck okay")

            for alignfile in content:
                # samtools sort [-l level] [-m maxMem] [-o out.bam] [-O format]
                # [-n] [-t tag] [-T tmpprefix] [-@ threads] [in.sam|in.bam|in.cram]
                try:
                    print("name sorting " + alignfile)
                    tail = os.path.split(alignfile)[1]
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
                    sorted_alignfiles.append(sorted_input)

            print("all sorted files = " + str(sorted_alignfiles))
            buff.write(u" --order name")

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
sorted_alignfiles = []
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
for file in sorted_alignfiles:
    os.remove(file)
sys.exit(retval)
