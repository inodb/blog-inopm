==========================================
M Dopson Viral Metagenomes Project
==========================================
:date: 2014-05-31 00:00
:summary: Viral metagenomes assemblies
:start_date: 2014-03-21
:end_date: 2014-09-31

Performing assemblies, mappings and some analysis for viral metagenomes. It
uses a lot of the `metassemble`_ scripts

**UPDATE 2014-09** Started doing binning with CONCOCT as well. Selecting only those bins which have no
microbial Single Copy Genes (SCGs).


Google docs
===========
`Assembly stats`_


Assemblies
============
Performed assemblies with Ray on `Lindgren`_ over kmers 31 to 81 with a stepsize of 10. First copied the files::
    
    rsync -va xxxx@xxxx.xxxx.xxx:/proj/b2013127/INBOX/M.Dopson_13_05/ .

Directory structure like that::
    
    $ ls
    assemblies
    P911_101
    P911_102
    P911_103
    P911_104
    P911_105
    P911_106

First did assemblies for P911_101, P911_102 and P911_106::
    
    cd assemlies
    for d in ../P911_10{1,2,6}; do
        mkdir -p ${d##.*/} && cd ${d##.*/}
        for k in `seq 31 10 81`; do
            qsub  -V -d `pwd` -o ray-$k-pbs.out -l procs=2048,walltime=24:00:00 \
                -v QSUB_ARGUMENTS="aprun -n 2048 Ray -k $k -o out_$k -p ../$d/*/4_*.fastq.gz -p ../$d/*/7_*.fastq.gz" \
                /cfs/klemming/nobackup/i/inodb/github/metassemble/bin/wrapper_jobscript.pbs
        done
        cd ..
    done

It uses two libraries, since those were resequenced. The wrapper_jobscript
executes whatever is in the ``QSUB_ARGUMENTS`` variable. Similarly for
P911_103, P911_104, P911_105, but with one library::

    for d in ../P911_10{3,4,5}; do
        reads=( $d/*/5_*.fastq.gz )
        mkdir -p ${d##.*/} && cd ${d##.*/}
        for k in `seq 31 10 81`; do
            qsub  -V -d `pwd` -o ray-$k-pbs.out -l procs=2048,walltime=24:00:00 \
            -v QSUB_ARGUMENTS="aprun -n 2048 Ray -k $k -o out_$k -p ../$d/*/5_*.fastq.gz" \
            /cfs/klemming/nobackup/i/inodb/github/metassemble/bin/wrapper_jobscript.pbs
        done
        cd ..
    done

Copied the files back to the original server::

    rsync -va assemblies xxxx@xxx:/proj/b2013127/nobackup/projects/M.Dopson_13_05/

Then combined the different kmer assemblies using Newbler::
    
    cd /proj/b2013127/nobackup/projects/M.Dopson_13_05/assemblies
    for dir in P911_{101,102,103,104,105,106}; do
        cd $dir
        sbatch --output=newbler-slurm.out -J merge-dopson -A b2013127 -t 2-00:00:00 -p core -n 8 \
            ~/bin/sbatch_job bash -x $METASSEMBLE_DIR/scripts/assembly/merge-asm-newbler.sh newbler \ 
            out_*/Contigs.fasta
        cd ..
    done

Which results in the following assemblies::

    $ ls */newbler/454AllContigs.fna
    P911_101/newbler/454AllContigs.fna  P911_103/newbler/454AllContigs.fna  P911_105/newbler/454AllContigs.fna
    P911_102/newbler/454AllContigs.fna  P911_104/newbler/454AllContigs.fna  P911_106/newbler/454AllContigs.fna

Mapping
======================

After the assemblies all reads were mapped back against every merged assembly::

    cd /proj/b2013127/nobackup/projects/M.Dopson_13_05/assemblies
    d=`pwd`
    for p in P911_10{1,2,3,4,5,6}; do
        mkdir -p $p/newbler/map
        cd $p/newbler/map
        for s in /proj/b2013127/INBOX/M.Dopson_13_05/P911_*/*/*_1.fastq.gz; do
            mkdir -p ${s##*/}
            cd ${s##*/}
            ls bowtie2/asm_pair-smds.coverage || \
                sbatch -A b2013127 -t 01-00:00:00 -J mdopson-map-$p -p core -n 4 ~/bin/sbatch_job \
                bash $METASSEMBLE_DIR/scripts/map/map-bowtie2-markduplicates.sh -ct 4 $s ${s/_1.fastq/_2.fastq} \
                pair ../454AllContigs.fna asm bowtie2
            cd ..
        done
        cd $d
    done

Binning
========================

We wanted to run CONCOCT and get only those bins out that don't have any microbial Single Copy Genes. Hopefully these
represent viral bins. Follows the `complete example`_ of the CONCOCT repository.

1. Cut up the assembly in 10K chunks::

    cd /proj/b2013127/nobackup/projects/M.Dopson_13_05/assemblies
    for d in P911_10{1,2,3,4,5,6}; do
        mkdir -p $d/newbler/concoct/cut_up_10K
        time python ~inod/glob/src/CONCOCT/scripts/cut_up_fasta.py -c 10000 -o 0 \
            -m $d/newbler/454AllContigs.fna > $d/newbler/concoct/cut_up_10K/contigs_c10K.fa &
    done

2. Rerun mapping on new contigs::

    cd /proj/b2013127/nobackup/projects/M.Dopson_13_05/assemblies
    d=`pwd`
    for p in P911_10{1,2,3,4,5,6}; do
        mkdir -p $p/newbler/concoct/map
        cd $p/newbler/concoct/map
        cp ../cut_up_10K/contigs_c10K.fa .
        bowtie2-build contigs_c10K.fa contigs_c10K.fa
        for s in /proj/b2013127/INBOX/M.Dopson_13_05/P911_*/*/*_1.fastq.gz; do
            mkdir -p ${s##*/}
            cd ${s##*/}
            ls bowtie2/asm_pair-smds.coverage || \
                sbatch -A b2013127 -t 01-00:00:00 -J mdopson-map-$p -p core -n 4 ~/bin/sbatch_job \
                bash $METASSEMBLE_DIR/scripts/map/map-bowtie2-markduplicates.sh -ct 4 $s ${s/_1.fastq/_2.fastq} \
                pair ../contigs_c10K.fa asm bowtie2
            cd ..
        done
        cd $d
    done

3. Generate input tables for CONCOCT::

    cd /proj/b2013127/nobackup/projects/M.Dopson_13_05/assemblies
    d=`pwd`;
    for p in P911_10{1,2,3,4,5,6}; do
        mkdir -p $p/newbler/concoct/concoct-input
        cd $p/newbler/concoct/concoct-input
        time python ~/glob/src/CONCOCT/scripts/gen_input_table.py \
            --samplenames <(for c in ../map/*/bowtie2/asm_pair-smds.coverage; do echo $c | cut -d/ -f3; done) \
            --isbedfiles ../map/contigs_c10K.fa ../map/*/bowtie2/asm_pair-smds.coverage > concoct_inputtable.tsv
        cut -f1,3-26 concoct_inputtable.tsv > concoct_inputtableR.tsv
        cd $d
    done

4. Run CONCOCT with different minimum contig lengths::

    cd /proj/b2013127/nobackup/projects/M.Dopson_13_05/assemblies
    d=`pwd`;
    for p in P911_10{1,2,3,4,5,6}; do
        cd $p/newbler/concoct
        for co in 700 1000 2000 3000; do
            grep -q 'FINISHED' concoct-output-$co-slurm.out ||
                sbatch -A b2013127 -p core -n 5 -t 1-00:00:00 -J $p-concoct-$co \
                    --output=concoct-output-$co-slurm.out ~/bin/sbatch_job concoct \
                    -l $co -c 400 -k 4 --coverage_file concoct-input/concoct_inputtableR.tsv \
                    --composition_file map/contigs_c10K.fa -b concoct-output-$co/
        done
        cd $d
    done

5. Run prodigal and rpsblast for each sample::

    cd /proj/b2013127/nobackup/projects/M.Dopson_13_05/assemblies
    d=`pwd`;
    for p in P911_10{1,2,3,4,5,6}; do
        cd $p/newbler/concoct
        mkdir -p annotations/cog-annotations/ annotations/proteins/
        sbatch --output=annotations/cog-annotations/rpsblast.out-slurm.out \
            -A b2013127 -J rpsblast_$p -t 1-00:00:00 -p core -n 1 \
            ~/bin/sbatch_job \
            prodigal -a annotations/proteins/contigs_c10K.faa \
            -i map/contigs_c10K.fa -f gff -p meta '>' \
            annotations/proteins/contigs_c10K.gff '&&' \
            rpsblast -outfmt \
            "'6 qseqid sseqid evalue pident score qstart qend sstart send length slen'" \
            -max_target_seqs 1 -evalue 0.001 -query annotations/proteins/contigs_c10K.faa \
            -db '/proj/b2010008/nobackup/database/cog_le/Cog' -out annotations/cog-annotations/rpsblast.out
        cd $d
    done

.. _Lindgren: https://www.pdc.kth.se/resources/computers/lindgren
.. _metassemble: https://github.com/inodb/metassemble
.. _Assembly stats: https://docs.google.com/spreadsheet/ccc?key=0Ammr7cdGTJzgdG4tb2tfMGpsX1UxeWlYX0pEaFQ5RGc&usp=drive_web#gid=0
.. _complete example: https://concoct.readthedocs.org/en/latest/complete_example.html
