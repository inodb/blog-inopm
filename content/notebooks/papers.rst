==========================================
Notes on papers
==========================================
:date: 2014-10-01 00:00
:summary: Short notes on read papers

Othologous Gene Clusters and Taxon Signature Genes for Viruses of Prokaryotes (2013)
====================================================================================
Summary

- Phage Orthologous Groups (POGs)
- 1,000 genomes, including genomes of dsDNA (88%), ssDNA (10%), ssRNA and dsRNA
  (2%). Also archael viruses (still calling it POG though). 93% of the dsDNA
  belonged to tailed phages of the order Caudovirales.
- *Orthologous groups* Edge-Search algorithm. Only E values of <10 and covering
  at least 50% of the protein lengths. Protein belonging to multiple groups is
  always an error (only 1% of all proteins).
- 57 taxa to find signature genes for. Only using those with at least 3
  distinct viruses and removing temporary collections or unclassified viruses.
  Used 100% precision (only correct genomes), then highest recall (found in most
  genomes).
- host listing in GenBank of archaeal and bacterial species
- COG-building method on 97,731 proteins (or domains) from 1,027 virus genomes
  were clustered into 4,542 POGs
- POG size from a minimum of 3 proteins from 3 distinct viruses up to 673
  proteins from 378 virus. Most of the POGs are small with with a median size
  of 5 proteins from 5 viruses
- no POG found in more than 37% of the 1,027 virus genomes. Only 1% of the 
  POGs are shared by more than a fifth of the genomes. Most distant
  connections by different genes, e.g. ssDNA Microviridae and Inoviridae 
  share a single different POG with dsDNA viruses
- *Functional classification of POGs* Substantial fraction including 10 of the
  top 100 larges POGs are completely uncharacterized.
- *Taxon signature gens* In file S5. Top-quality POG signatures in Table 1.


Personal Notes

- *Bacillus* phage G, largest known phage genome - Two methods of viral
  reproduction: lysogenic cycle and lytic cycle - Caudoviralis (caudo means
  tail, order of viruses). No sequence similarity for DNA or amino acids of
  families in that order, just morphology.
- `Inovirus <http://viralzone.expasy.org/all_by_species/558.html>`_ (nos means
  muscle in Greek). ssVirus
