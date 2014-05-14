==========================================
CONCOCT Project
==========================================
:date: 2004-10-03 10:20
:summary: CONCOCT paper

Performing assemblies, mappings and some analysis for the `CONCOCT paper`_.
Code can be found at: https://github.com/BinPro/CONCOCT


.. _CONCOCT paper: http://arxiv.org/abs/1312.4038


Google docs
===========
https://drive.google.com/?authuser=0#folders/0B2mr7cdGTJzgQmE1aUZwZ2s3UWs


Assemblies
===========
https://docs.google.com/spreadsheets/d/1fDZjgK43Rg-Wn2zU1P_IbxPh7ZwXgdmcmMvKl9gJNek/edit#gid=0
* NewMock{1,2,2b} - Performed on Lindgren
* Sharon2013 - Performed on Milou


Mapping
======================
Used these crazy one-liners::

    # map all reads
    d=`pwd`; for s in ../../NewMock2/Sorted_Sample*R1*.fasta.gz; do mkdir -p ${s##.*/}; cd ${s##.*/}; ls bowtie2/asm_pair-smds.coverage || sbatch -d afterok:1735572 -A b2010008 -t 12:00:00 -J NewMock1-ref-map -p core -n 4 ~/bin/sbatch_job bash $METASSEMBLE_DIR/scripts/map/map-bowtie2-markduplicates.sh -ct 4 -p '-f' ../$s ../${s/R1/R2} pair ../ref.fa asm bowtie2; cd $d; done
    
    # check for completion of coverage generation
    find /proj/b2013151/nobackup/private/per-sample-asm -name *.coverage | parallel grep -q 'genome' {} '||' echo no genome in {}

MetaWatt v 1.7
==================
Used GBK files to build reference database (includes Bacteria and Archaea):

ftp://ftp.ncbi.nlm.nih.gov/genomes/Bacteria/all.gbk.tar.gz

Explanation is in the README of MetaWatt:

http://sourceforge.net/projects/metawatt/files/

We cut up contigs in 10K and filtered contigs < 1K out. Then simply chose a bin
size that resulted in the expected number of bins for high confidence binning.

* NewMock1
  high confidence 20 clusters min bin size 1900 kb
* NewMock2
  high confidence 101 clusters min bin size ??
* Sharon2013
  high confidence 34 clusters min bin size 110 kb

Used to extract the clusters::
    
    less Contigs.fasta.data | grep '^#con' | grep '     All     ' | awk -v OFS=',' '{print $1,$3}' | sed 's/Sharon2013_high_bin_//' | sed 's/^#//' > high_confidence.csv '
