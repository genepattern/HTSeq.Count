#!/usr/bin/env python3

from io import StringIO
import os
import subprocess
from subprocess import PIPE
import sys

import pysam


def generate_command():
    buff = StringIO()
    buff.write(u"htseq-count ")
    buff.write(u"--input input.files.list ")

    allargs = iter(sys.argv[1:])
    for arg in allargs:
        # NOTE need to return the array to use globally
        if arg.startswith('--input'):
            # should be a file list
            val = next(allargs, None)

            with open(val) as f:
                content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [alignfile.strip() for alignfile in content]
            print("content = " + str(content))

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
                    print('alignfile = ' + alignfile)

                # file extension check/format detection
                # This can be removed in a future version when
                # htseq-count no longer requires a parameter it is ignoring...
                print("determining file extension")
                exts = [os.path.splitext(alignfile)[1]]
                basename = os.path.splitext(alignfile)[0]
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
                        print("All extensions are the same")
                        global file_format
                        file_extension = exts[0]
                        file_format = file_extension.replace(".", "")
                        print("input format is " + file_format)
                        buff.write(u"--format ")
                        buff.write(file_format)
                print("name sorting input")
                # samtools sort [-l level] [-m maxMem] [-o out.bam] [-O format]
                # [-n] [-t tag] [-T tmpprefix] [-@ threads] [in.sam|in.bam|in.cram]
                global sorted_input
                try:
                    pysam.sort(
                        "-o",
                        basename + "_nameSort" + "." + file_format,
                        "-n",
                        alignfile)
                except:
                    print(pysam.sort.getMessage())
                else:
                    print("sorted")
                    sorted_input = basename + "_nameSort" + "." + file_format
                    buff.write(u" --order name")
                    print(sorted_input)

            all_inputs = [sorted_input]
            print("These are all the sorted inputs " + str(all_inputs))

            # write the sorted files back into the expected GP file list
            f = open("input.files.list", "w")
            for ele in all_inputs:
                f.write(ele + '\n')
            f.close()

            return buff.getvalue()


# get the original command line
orig_cmd = str(sys.argv[1:])
print("Original command line was " + orig_cmd)

# Make new command line with sorted_input
# & file_extension converted to the default value for format on the new command line.
new_cmd = generate_command() + str(sys.argv[5:])
print(new_cmd)

childProcess = subprocess.Popen(new_cmd, shell=True, env=os.environ, stdout=PIPE, stderr=PIPE)
stdout, stderr = childProcess.communicate()
retval = childProcess.returncode
if retval != 0:
    # if non-zero return, print stderr to stderr
    print(stdout)
    print(stderr, file=sys.stderr)

sys.exit(retval)
