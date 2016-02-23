HTSeq 0.6.1p2: Counting reads in features with 'htseq-count'.

---------------------------------------------------------------------
Note: This is a Broad hosted only wrapper module which uses the 
following dotkits: 
    'Python-2.7' and '.htseq-0.6.1-python-2.7.1-sqlite3-rtrees'
---------------------------------------------------------------------

---------------------------------------------------------------------
    ./htseq-count --help output
---------------------------------------------------------------------
Usage: htseq-count [options] alignment_file gff_file

This script takes an alignment file in SAM/BAM format and a feature file in
GFF format and calculates for each feature the number of reads mapping to it.
See http://www-huber.embl.de/users/anders/HTSeq/doc/count.html for details.

Options:
  -h, --help            show this help message and exit
  -f SAMTYPE, --format=SAMTYPE
                        type of <alignment_file> data, either 'sam' or 'bam'
                        (default: sam)
  -r ORDER, --order=ORDER
                        'pos' or 'name'. Sorting order of <alignment_file>
                        (default: name). Paired-end sequencing data must be
                        sorted either by position or by read name, and the
                        sorting order must be specified. Ignored for single-
                        end data.
  -s STRANDED, --stranded=STRANDED
                        whether the data is from a strand-specific assay.
                        Specify 'yes', 'no', or 'reverse' (default: yes).
                        'reverse' means 'yes' with reversed strand
                        interpretation
  -a MINAQUAL, --minaqual=MINAQUAL
                        skip all reads with alignment quality lower than the
                        given minimum value (default: 10)
  -t FEATURETYPE, --type=FEATURETYPE
                        feature type (3rd column in GFF file) to be used, all
                        features of other type are ignored (default, suitable
                        for Ensembl GTF files: exon)
  -i IDATTR, --idattr=IDATTR
                        GFF attribute to be used as feature ID (default,
                        suitable for Ensembl GTF files: gene_id)
  -m MODE, --mode=MODE  mode to handle reads overlapping more than one feature
                        (choices: union, intersection-strict, intersection-
                        nonempty; default: union)
  -o SAMOUT, --samout=SAMOUT
                        write out all SAM alignment records into an output SAM
                        file called SAMOUT, annotating each line with its
                        feature assignment (as an optional field with tag
                        'XF')
  -q, --quiet           suppress progress report

Written by Simon Anders (sanders@fs.tum.de), European Molecular Biology
Laboratory (EMBL). (c) 2010. Released under the terms of the GNU General
Public License v3. Part of the 'HTSeq' framework, version 0.6.1p1.
