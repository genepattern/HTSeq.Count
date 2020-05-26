FROM biocontainers/htseq:v0.11.2-1-deb-py3_cv1

USER root
RUN mkdir /htseq_count
RUN chown biodocker /htseq_count
USER biodocker
COPY htseq_count_wrapper.pl /htseq_count/htseq_count_wrapper.pl

ENTRYPOINT []

 
