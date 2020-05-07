FROM biocontainers/htseq:v0.11.2-1-deb-py3_cv1

RUN mkdir /htseq_count
COPY htseq_count_wrapper.pl /htseq_count/htseq_count_wrapper.pl

ENTRYPOINT []

 
