#!/usr/bin/env python

from Bio import SeqIO
from Bio.Blast import NCBIXML


resblast = open('blast_res.xml','r')
result = NCBIXML.parse(resblast)

best = 0
score_max = 0

for seq in result :
	for desc in seq.descriptions:
		print('titre de la desc: ',desc.title)
		print('score du meilleur HSP de la desc: ',desc.score)
		print('nombre d HSP: ',desc.num_alignments)
