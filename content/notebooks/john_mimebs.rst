==========================================
MIMEBS Project
==========================================
:date: 2004-10-03 10:20
:summary: Assembly and mapping of MIMEBS

Performing assemblies for the `MIMEBS project`_. Working through BILS, mainly
for John Larsson.


.. _MIMEBS project: http://birgittabergman.wordpress.com/2013/03/11/mimebs-environmental-genome-shotgun-sequencing-of-microbial-populations-in-the-baltic-sea/

Assemblies
===========
Performed one assembly per filter, because a combined assembly didn't work.
Results in:

https://docs.google.com/spreadsheet/ccc?key=0Ammr7cdGTJzgdEVuWUNIeEo2Y3hvMkloM0hhaUJWaXc#gid=1


Mapping
======================
Mapped every sample against every other sample.

* Changed .coverage.percontig to include all contigs
* Changed samtools index to decrease chance of race condition
