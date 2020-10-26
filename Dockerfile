FROM biocontainers/htseq:v0.11.2-1-deb-py3_cv1

USER root
RUN mkdir /htseq_count
RUN chown biodocker /htseq_count
USER biodocker
COPY htseqcount_input_detect_and_sort.py /htseq_count/htseqcount_input_detect_and_sort.py

ENTRYPOINT []

 
