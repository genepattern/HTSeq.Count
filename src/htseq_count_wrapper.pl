use Getopt::Long;

GetOptions(\%options,
  "htseqcount=s", # --htseqcount <HTSEQ> must be on command line
  "input=s", # is always input.files.list
  "format=s", # sam (default) or bam
  "names=s", # optional
  "gtf=s", # an ftp object
  "order=s", # name (default) or pos
  "strand=s", # no, yes (default) or reverse
  "minqual=i",
  "featuretype=s",
  "idtype=s",
  "mode=s", # union (default), intersection-strict or intersection-nonempty
  "nonunique=s", # none (default) or all
  "secondary=s", # score (default) or ignore
  "supplementary=s", # score (default) or ignore
  "genename=s", # optional
  "output=s",
  "outformat=s" # htseq (default), excel or gct
);

# start writing command line and add options
# if extra table is asked for, remember this for later in the script
$cmd = "$options{htseqcount} -q";
  # set quiet to prevent progress of run to be sent to standard output
$cmd .= " -f $options{format} -r $options{order} -s $options{strand} -a $options{minqual} -m $options{mode} --nonunique=$options{nonunique} --secondary-alignments=$options{secondary} --supplementary-alignments=$options{supplementary} -t $options{featuretype} -i $options{idtype}";
if ($options{genename} ne '') {
  $extratable = 1;
  $extratable_header = $options{genename};
  $extratable_header =~ s/_/ /g;
  $cmd .= " --additional-attr=$options{genename}";
}

# add SAM/BAM file names and GTF file name to the command line
open IN, $options{input};
while (<IN>) {
  chomp;
  $cmd .= " $_";
  $Nfiles++;
}
close IN;
$cmd .= " $options{gtf}";

# if Excel or GCT format is asked for, make a tab-separated list of sample
# names and store it in $nameslist.
if ($options{outformat} ne 'htseq') {
  if ($options{names} ne '') {
    open IN, "$options{names}";
    while (<IN>) {
      chomp;
      $nameslist .= "\t$_";
      $Nnames++;
    }
    close IN;
    if ($Nfiles != $Nnames) {
      die "Number of input files with mappings and number of names in $options{names} are not the same !\n";
    }
  } else {
    open IN, $options{input};
    while (<IN>) {
      chomp;
      $_ =~ s/^.*\///;
      $_ =~ s/\.[sb]am$//i;
      $nameslist .= "\t$_";
    }
    close IN;
  }
}
# print "$nameslist\n"; # for debugging

# complete command line and start run
# if HTSeq raw format is asked, just run
# if Excel format is asked, write header in output and append HTSeq file
# if GCT format is asked, write HTSeq data in temporary file
if ($options{outformat} eq 'htseq') {
  $cmd .= " > $options{output}";
} elsif ($options{outformat} eq 'excel') {
  open OUT, ">$options{output}";
  print OUT 'gene ID';
  if ($extratable) {
    print OUT "\t${extratable_header}";
  }
  print OUT "$nameslist\n";
  close OUT;
  $cmd .= " >> $options{output}";
} elsif ($options{outformat} eq 'gct') {
  $cmd .= ' > TMP_OUTPUT';
}
# print "$cmd\n"; # for debugging
system $cmd;

# if GCT format is asked, first count the number of lines with counts,
# then write the output. if no extra table is provided, add a dummy
if ($options{outformat} eq 'gct') {
  open IN, 'TMP_OUTPUT';
  while (<IN>) {
    if ($_ !~ /^__/) { $Nlines++ }
  }
  close IN;
  open OUT, ">$options{output}.gct";
  print OUT "#1.2\n";
  print OUT "$Nlines\t$Nnames\n";
  print OUT 'gene ID';
  if ($extratable) {
    print OUT "\t${extratable_header}";
  } else {
    print OUT "\tdummy";
  }
  print OUT "$nameslist\n";
  open IN, 'TMP_OUTPUT';
  if ($extratable) {
    while (<IN>) {
      if ($_ !~ /^__/) { print OUT $_ }
    }
  } else {
    while (<IN>) {
      if ($_ =~ /^__/) {
        print STDOUT $_;
      } else {
        $_ =~ s/\t/\tNA\t/;
        print OUT $_;
      }
    }
  }
  close IN;
  close OUT;
  unlink 'TMP_OUTPUT', $options{input};
}