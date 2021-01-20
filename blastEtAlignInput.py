#!/usr/bin/python
import os
import sys
import time
from Bio import Entrez
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import AlignIO
from Bio.Align.Applications import ClustalOmegaCommandline

Entrez.email = "aaa@aaa.fr"
print("Merci d entrez 1 pour le blast via le web ou 2 pour le blast en local.")
b = input()
#pour laisser le choix du blast a l utilisateur

progress=0
def progressBar(count,total,status=""):
	bar_len=60
	filled_len=int(round(bar_len*count/float(total)))

	percents=round(100.0*count/float(total),1)
 	bar='='*filled_len+'-'*(bar_len - filled_len)

	sys.stdout.write('[%s]%s%s...%s\r'%(bar,percents,'%',status))
	sys.stdout.flush()
#mise en place de la barre de chargement


if b == 1:
	print("Vous avez selectionne le blast via le web. Patience!")
	#BlastWeb.py
	liste_id = ['XM_004872686.1','XM_003475766.1','XM_004637847.2','XM_005411935.2','NG_008353.1']
	cpt=0
	blast_res = open('blast_res.xml','a') #on cree et ouvre le fichier resultat
	while cpt != len(liste_id):
		with open('fichierABlast',"w") as fd:
			fic_seq = Entrez.efetch(db="Nucleotide", id=liste_id[cpt], rettype="fasta")
			seq = SeqIO.read(fic_seq,'fasta')
			res_xml = NCBIWWW.qblast('blastn', 'nt', seq.format('fasta'))
			blast_res.writelines(res_xml) #ecriture directement de la seq blastee dans le fichier resultat
			print'Ajout de la sequence KRT85 blastee de ',liste_id[cpt],' dans le fichier blast_res.xml .'
			fic_seq.close()
			res_xml.close()
			os.remove('fichierABlast') #on ferme tout pour ne pas avoir de doublons lors du prochain tour de boucle
			cpt = cpt+1 #pour parcourir la liste d ID, obligatoire vu que impossible de recuperer les seq autrement

	print('Le blast via le web est termine')


if b == 2:
	print("Vous avez selectionne le blast en local.")
	comparaison = NcbiblastnCommandline(query="out.fasta", db="basename", evalue=100000000000000000000000000, outfmt=5, out="blast_res.xml")
	myStdout, myStderr = comparaison()
	print("Le blast local est termine, ses resultats sont dans le fichier blast_res.xml.")


#alignio.py
print("Lancement de l'alignement")
fichierEntree = "out.fasta"
fichierSortie = "aligne.fasta"

commande = ClustalOmegaCommandline(infile=fichierEntree, outfile=fichierSortie, force =True)
myStdout, myStderr = commande()

mon_aln = AlignIO.read(fichierSortie, 'fasta')
print("Nombre de seq de l alignement: ",len(mon_aln))
print("ID des sequecences: ")
for alignedSeq in mon_aln: #pour parcourir l alignement et faire avancer la barre de progression en meme temps
        print(alignedSeq.id)
        if progress <100:
			for j in range (0,10):
				progress +=1
				progressBar(progress, 100)
				time.sleep(0.05)
while progress <100:
	progress +=1
	time.sleep(0.03)
	progressBar(progress,100)

print("L alignement est fait")


os.remove("basename.nhd")
os.remove("basename.nhi")
os.remove("basename.nhr")
os.remove("basename.nin")
os.remove("basename.nog")
os.remove("basename.nsd")
os.remove("basename.nsi")
os.remove("basename.nsq") #pour ne garder qu un fichier resultat final et non toute la db
os.remove("out.fasta") #pour eviter les doublons si le programme est lance plusieur fois d affile 
