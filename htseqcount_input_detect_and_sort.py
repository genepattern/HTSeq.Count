#!/usr/bin/env python3


from io import StringIO
import os
import subprocess
from subprocess import PIPE, STDOUT
import sys

import pysam

# commandLine=/htseq_count/htseqcount_input_detect_and_sort.py --htseqcount htseq-count --input <input.files> <sample.names> --gtf <GTF.file> --strand <strandedness> --minqual <min.qual> --mode <mode> --nonunique <count.nonunique> --secondary <count.secondary> --supplementary <count.supplementary> --featuretype <feature.type> --idtype <id.type> <gene.name> --output <output.file> --outformat <output.format>

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

                    # check that all extensions are the same
                    all_extensions = exts
                    check = True

                    for x in exts:
                        if all_extensions != x:
                            check = False
                            print("Files are not of the same format")
                            break

                        if check:
                            print("All extensions are the same")
                            file_extension = exts[1]
                            print("input is " + file_extension)
                            buff.write(u"--format")
                            buff.write(unicode(file_extension))

                            return file_extension

                    # samtools sort [-l level] [-m maxMem] [-o out.bam] [-O format]
                    # [-n] [-t tag] [-T tmpprefix] [-@ threads] [in.sam|in.bam|in.cram]
                    sorted_input = [pysam.sort(
                        "-o",
                        alignfile + "_nameSort" + file_extension,
                        "-n",
                        alignfile)]
                    print('sorted')
                    print("sorted file name is " + alignfile + "_nameSort" + file_extension)
                    buff.write(u"--order name")

                    return sorted_input

                # write the sorted files back into the expected GP file list
                f = open('input.files.list', 'w')
                for ele in sorted_input:
                    f.write(ele + '\n')
                f.close()

                buff.write(u"--input input.files.list")


# get the original command line
orig_cmd = str(sys.argv[1:])
print("Original command line was " + orig_cmd)

# Make new command line with sorted_input
# & file_extension converted to the default value for format on the new command line.
#allargs = iter(sys.argv)
#next(allargs)
new_cmd = generate_command()
print(new_cmd)

childProcess = subprocess.Popen(new_cmd, shell=True, env=os.environ, stdout=PIPE, stderr=PIPE)
stdout, stderr = childProcess.communicate()
retval = childProcess.returncode
if retval != 0:
    # if non-zero return, print stderr to stderr
    print(stdout)
    print >> sys.stderr, stderr
#else:
    # if not a non-zero stdout, print stderr to stdout since Hisat2Indexer logs non-error
    # stuff to stderr.  Downside is the stderr and stdout are not interlevened
    #print(stdout)
    #print(stderr)

sys.exit(retval)

