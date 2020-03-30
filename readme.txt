HTSeq 0.11.2: Counting reads in features with 'htseq-count'.

----------------------------------------------------------------------------------------------
This module uses the biocontainers HTSeq.count image biocontainers/htseq:v0.11.2-1-deb-py3_cv1
----------------------------------------------------------------------------------------------

usage: htseq-count [options] alignment_file gff_file

This script takes one or more alignment files in SAM/BAM format and a feature
file in GFF format and calculates for each feature the number of reads mapping
to it. See http://htseq.readthedocs.io/en/master/count.html for details.

positional arguments:
  samfilenames          Path to the SAM/BAM files containing the mapped reads.
                        If '-' is selected, read from standard input
  featuresfilename      Path to the file containing the features

optional arguments:
  -h, --help            show this help message and exit
  -f {sam,bam}, --format {sam,bam}
                        type of <alignment_file> data, either 'sam' or 'bam'
                        (default: sam)
  -r {pos,name}, --order {pos,name}
                        'pos' or 'name'. Sorting order of <alignment_file>
                        (default: name). Paired-end sequencing data must be
                        sorted either by position or by read name, and the
                        sorting order must be specified. Ignored for single-
                        end data.
  --max-reads-in-buffer MAX_BUFFER_SIZE
                        When <alignment_file> is paired end sorted by
                        position, allow only so many reads to stay in memory
                        until the mates are found (raising this number will
                        use more memory). Has no effect for single end or
                        paired end sorted by name
  -s {yes,no,reverse}, --stranded {yes,no,reverse}
                        whether the data is from a strand-specific assay.
                        Specify 'yes', 'no', or 'reverse' (default: yes).
                        'reverse' means 'yes' with reversed strand
                        interpretation
  -a MINAQUAL, --minaqual MINAQUAL
                        skip all reads with alignment quality lower than the
                        given minimum value (default: 10)
  -t FEATURETYPE, --type FEATURETYPE
                        feature type (3rd column in GFF file) to be used, all
                        features of other type are ignored (default, suitable
                        for Ensembl GTF files: exon)
  -i IDATTR, --idattr IDATTR
                        GFF attribute to be used as feature ID (default,
                        suitable for Ensembl GTF files: gene_id)
  --additional-attr ADDITIONAL_ATTR
                        Additional feature attributes (default: none, suitable
                        for Ensembl GTF files: gene_name). Use multiple times
                        for each different attribute
  -m {union,intersection-strict,intersection-nonempty}, --mode {union,intersection-strict,intersection-nonempty}
                        mode to handle reads overlapping more than one feature
                        (choices: union, intersection-strict, intersection-
                        nonempty; default: union)
  --nonunique {none,all}
                        Whether to score reads that are not uniquely aligned
                        or ambiguously assigned to features
  --secondary-alignments {score,ignore}
                        Whether to score secondary alignments (0x100 flag)
  --supplementary-alignments {score,ignore}
                        Whether to score supplementary alignments (0x800 flag)
  -o SAMOUTS, --samout SAMOUTS
                        write out all SAM alignment records into SAM files
                        (one per input file needed), annotating each line with
                        its feature assignment (as an optional field with tag
                        'XF')
  -q, --quiet           suppress progress report

Written by Simon Anders (sanders@fs.tum.de), European Molecular Biology
Laboratory (EMBL). (c) 2010. Released under the terms of the GNU General
Public License v3. Part of the 'HTSeq' framework, version 0.11.2.