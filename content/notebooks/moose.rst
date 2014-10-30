==========================================
Moose Project
==========================================
:date: 2013-04-01 00:00
:summary: Assembly and mapping of Moose
:start_date: 2013-04-01
:end_date: 2014-08-31

Performing assemblies for the moose project. Working through BILS, mainly for
Anders Andersson.


Assemblies
===========
https://docs.google.com/a/scilifelab.se/spreadsheet/ccc?key=0Ammr7cdGTJzgdHdpVVB3VnVSNVR1RlJDSUpad2tOSlE#gid=4

Separate Ray assemblies on Lindgren
===================================
Assembled three samples 102, 105 and 106 separately with Ray on Lindgren e.g. for 102::

    cd /cfs/klemming/nobackup/i/inodb/moose/sep-assemblies-lindgren/102 
    for k in 41 51 61 71 81; do
        qsub -V -d `pwd` -o out_$k-pbs.out -l procs=1024,walltime=04:00:00 -v \
            QSUB_ARGUMENTS="aprun -n 1024 Ray-2.3.1-k${k} -k $k -o out_$k $(echo $(for s in ../../A.Andersson_12_01/*/*/*$(basename `pwd`)*_1.fastq; do echo -p $s ${s/_1.fastq/_2.fastq}; done))" \
            /cfs/klemming/nobackup/i/inodb/github/metassemble/bin/wrapper_jobscript.pbs
    done

All were successful::

    $ for f in */out_*-pbs.out; do tail -10 $f | grep -q FINISHED && echo $f finished; done
    102/out_41-pbs.out finished
    102/out_51-pbs.out finished
    102/out_61-pbs.out finished
    102/out_71-pbs.out finished
    102/out_81-pbs.out finished
    105/out_41-pbs.out finished
    105/out_51-pbs.out finished
    105/out_61-pbs.out finished
    105/out_71-pbs.out finished
    105/out_81-pbs.out finished
    106/out_41-pbs.out finished
    106/out_51-pbs.out finished
    106/out_61-pbs.out finished
    106/out_71-pbs.out finished
    106/out_81-pbs.out finished


Merge assemblies on Milou
=========================
They were afterward copied to the milou cluster::
    
   rsync -r --progress -av sep-assemblies-lindgren inod@milou1.uppmax.uu.se:/gulo/proj_nobackup/b2010008/projects/moose/metassemble/ 

and merged using Newbler::

    for dir in 102 105 106; do
        cd $dir
        sbatch --output=newbler-slurm.out -J merge-moose -A b2010008 -t 2-00:00:00 -p core -n 8 \
            ~/bin/sbatch_job bash -x $METASSEMBLE_DIR/scripts/assembly/merge-asm-newbler.sh newbler out_*/Contigs.fasta
        cd ..
    done

**UPDATE 2014-09**
Moved on with this project on `a separate GitHub repo <https://github.com/inodb/2014-09-haspeborg-moose-project>`_.
