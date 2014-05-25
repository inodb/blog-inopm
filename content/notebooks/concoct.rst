==========================================
CONCOCT Project
==========================================
:date: 2014-05-31 00:00
:summary: CONCOCT paper
:start_date: 2014-07-01
:end_date: 2014-05-31

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
Used these crazy oneliners::

    # map all reads
    d=`pwd`; for s in ../../NewMock2/Sorted_Sample*R1*.fasta.gz; do mkdir -p ${s##.*/}; cd ${s##.*/}; ls bowtie2/asm_pair-smds.coverage || sbatch -d afterok:1735572 -A b2010008 -t 12:00:00 -J NewMock1-ref-map -p core -n 4 ~/bin/sbatch_job bash $METASSEMBLE_DIR/scripts/map/map-bowtie2-markduplicates.sh -ct 4 -p '-f' ../$s ../${s/R1/R2} pair ../ref.fa asm bowtie2; cd $d; done
    
    # check for completion of coverage generation
    find /proj/b2013151/nobackup/private/per-sample-asm -name *.coverage | parallel grep -q 'genome' {} '||' echo no genome in {}

    # copy mapping stats
    for s in NewMock2b/out_41/remap/*/*.out; do cat $s | head -50 | awk -v sample=`echo ${s} | cut -d/ -f4` -v OFS="\t" '{if ($0 ~ "were paired") {a = $1;} if ($0 ~ ") aligned concordantly 0 times") { b = $1} if ($0 ~ ") aligned concordantly exactly 1 time" ) {c = $1} if ($0 ~ "aligned concordantly >1 times") { d=$1 } if ($0 ~ ") aligned 0 times") {e=$1} if ($0 ~ "% overall alignment rate") { f = $1 } } END { print sample,a,b,c,d,e,f }'; done' } }")" }"") }}'

    # copy duplication stats
    find . -name *.metrics | sort -k5 -t_ | xargs -n1 awk '{if (NR==8) {print $3}}'

Generate CONCOCT input files
=============================
Generate the input table for CONCOCT after mapping::

    sbatch -t 06:00:00 -A b2010008 -p core -n 8 -J gen_input_table --output=concoct_inputtable_4f4685e.tsv-slurm.out ~/bin/sbatch_job time python /glob/inod/github/CONCOCT/scripts/gen_input_table.py --isbedfiles --samplenames '<(for s in *_1.fastq.gz; do echo ${s%%_1.fastq.gz}; done)' Contigs.fasta *.fastq.gz/bowtie2/asm_pair-smds.coverage '>' concoct_inputtable_4f4685e.tsv

Generate the linkage table::

     sbatch -A b2010008 -J ecoli-linkage -t 06:00:00 -p node -n 16 --output=concoct_linkage_4f4685e.tsv-slurm.out ~/bin/sbatch_job time python /glob/inod/github/CONCOCT/scripts/bam_to_linkage.py -m 16 --samplenames '<(for s in *.fastq.gz; do echo ${s%%_1.fastq.gz}; done)' --fullsearch --regionlength 500 Contigs.fasta *.fastq.gz/bowtie2/asm_pair-smds.bam '>' concoct_linkage_4f4685e.tsv

Generate read counts for simulated mock data for contig to genome assignments::

    sbatch -A b2010008 -p node -n 16 -t 02:00:00 -J newmock1-41-count --output=contig_count_per_genome_4f4685e.tsv-slurm.out ~/bin/sbatch_job time python /glob/inod/github/CONCOCT/scripts/contig_read_count_per_genome.py -m 16 Contigs.fasta ../../../ref.fa Sorted*/bowtie2/asm_pair-smds.bam '>' contig_count_per_genome_4f4685e.tsv



Copying files between servers
==============================
Pretty useful to copy files between servers while keeping full path of the file::

    rsync --relative --progress -avhe 'ssh -p 99999' `find NewMock2b/ -regex '.*\(Contigs.fasta\|concoct_.*.tsv.*\|contig_count_per_genome.*.tsv.*\)'` ino@xx.xx.xx:/home/ino/projects/concoct-paper-assemblies/concoct-paper-assemblies/

    

Cutting up contigs
=====================
We found that cutting up contigs in pieces of 10K improved the binning::

    time python ~/gitrepos/biorhino-tools/scripts/br-cut-up-fasta.py -c 10000 -o 0 -m Contigs.fasta

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


Checking metagenome coverage and contig assignment
==========================================================
We are not able to get more genomes out than we assembled so it is good to look
at the actual coverage of the metagenome, see the notebook_. We used MUMmer for
the alignment::

    d=`pwd`; for c in out_41/Contigs.fasta; do mkdir -p ${c%%/*}/mummer && sbatch --output=${c%%/*}/mummer-slurm.out -p core -n 4 -A b2010008 -t 01-00:00:00 -J mummer-NewMock2b-${c%%/*} ~/bin/sbatch_job bash -x /glob/inod/github/metassemble/scripts/validate/nucmer/run-nucmer.sh genomes_above25_80_new_final.fasta $c ${c%%/*}/mummer/nucmer; cd $d; done

Duplication problem in Ray
============================
Stumbled on a duplication problem for F Prau. See also the notebook_. We checked duplication with MUMmer::

    for c in AnotherMock1/out_41/Contigs.fasta; do mkdir -p ${c%/*}/mummer-dup && sbatch --output=${c%/*}/mummer-dup-slurm.out -p core -n 4 -A b2010008 -t 5:00:00 -J mummer-dup-${c%/*} ~/bin/sbatch_job bash -x /glob/inod/github/metassemble/scripts/validate/nucmer/run-nucmer.sh $c $c ${c%/*}/mummer-dup/nucmer; cd $d; done

Then removed duplicate contigs with this gist:

.. raw:: html

  <script src="https://gist.github.com/inodb/80557dadf991fd4a038b.js"></script>

.. _notebook: http://nbviewer.ipython.org/github/inodb/notebooks/blob/master/concoct/metagenome-coverage-mocks.ipynb 
