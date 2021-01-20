#!/usr/bin/python

import os
import time
import sys
from Bio import Entrez
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import AlignIO
from Bio.Align.Applications import ClustalOmegaCommandline

Entrez.email= "aaa@aaa.fr"

#mise en place de la barre de chargement
def progressBar(count,total,status=""):
	bar_len=60
	filled_len=int(round(bar_len*count/float(total)))

	percents=round(100.0*count/float(total),1)
 	bar='='*filled_len+'-'*(bar_len - filled_len)

	sys.stdout.write('[%s]%s%s...%s\r'%(bar,percents,'%',status))
	sys.stdout.flush()


#attrapeletruc.py
liste_id = ['XM_004872686.1','XM_003475766.1','XM_004637847.2','XM_005411935.2','NG_008353.1']
cpt=0

progress=0

with open("out_multiseq.fasta","a") as fd: #on cree et ouvre notre fichier multiseq
	while cpt != len(liste_id):
		fic_seq = Entrez.efetch(db="Nucleotide", id=liste_id[cpt], rettype="fasta")
		fd.writelines(fic_seq) #on ecrit seq par seq dans le fichier resultat
		cpt = cpt+1
		if progress <50:
			for j in range (0,5):
				progress +=1
				progressBar(progress, 100)
				time.sleep(0.05) #on fait avancer la barre de progression avec l ecriture du fichier
while progress <50:
	progress +=1
	time.sleep(0.03)
	progressBar(progress,100)
#on parse le fichier resulat
Multiseq = SeqIO.parse('out_multiseq.fasta', 'fasta')

with open('out.fasta',"w") as fd:
	for seq in Multiseq:
		print(seq.format('fasta'))
		fd.write(seq.format('fasta'))
		if progress <100:
			for j in range (0,5):
				progress +=1
				progressBar(progress, 100)
				time.sleep(0.05)
#pour faire terminer la barre de chargement on ecrit nos sequence apres parse dans un nouveau fichier multiseq
while progress <100:
	progress +=1
	time.sleep(0.03)
	progressBar(progress,100)

os.remove("out_multiseq.fasta") #pour eviter les doublons
