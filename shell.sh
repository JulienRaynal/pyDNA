#!/bin/bash

echo "Lancement du programme"
python ./chopeEtParse.py

makeblastdb -in out.fasta -out basename -dbtype 'nucl' -hash_index

python ./blastEtAlignInput.py
#python ./nombreHSP.py
seaview ./aligne.fasta &
display ./swole_boy.jpg &

echo "Merci d'avoir utilisé notre programme!"
