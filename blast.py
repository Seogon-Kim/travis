import os
import sys
from os.path import expanduser

if __name__ == '__main__':
    home = expanduser("~")
    os.chdir(home)
    os.system("mkdir blast_example")
    os.chdir(home + "/blast_example")
    os.system("wget http://www.uniprot.org/uniprot/P04156.fasta")
    os.system("curl -O ftp://ftp.ncbi.nih.gov/refseq/D_rerio/mRNA_Prot/zebrafish.1.protein.faa.gz")
    os.system("gunzip zebrafish.1.protein.faa.gz")
    os.system("docker run -v " + home + "/blast_example" + ":/data/ biocontainers/blast:v2.2.31_cv2 makeblastdb -in zebrafish.1.protein.faa -dbtype prot")
    os.chdir(home)
    os.system("sudo chmod 777 blast_example")
    os.chdir(home + "/blast_example")
    os.system("docker run -v" + home + "/blast_example" + ":/data/ biocontainers/blast:v2.2.31_cv2 blastp -query P04156.fasta -db zebrafish.1.protein.faa -out results.txt")

    os.chdir(home)
    os.system("mkdir blast_example")
    os.chdir(home + "/blast_example")
    os.system("wget http://www.uniprot.org/uniprot/P04156.fasta")
    os.system("curl -O ftp://ftp.ncbi.nih.gov/refseq/D_rerio/mRNA_Prot/zebrafish.1.protein.faa.gz")
    os.system("gunzip zebrafish.1.protein.faa.gz")
    os.system("docker run -v " + home + "/blast_example" + ":/data/ biocontainers/blast:v2.2.31_cv2 makeblastdb -in zebrafish.1.protein.faa -dbtype prot")
    os.chdir(home)
    os.system("sudo chmod 777 blast_example")
    os.chdir(home + "/blast_example")
    os.system("docker run -v" + home + "/blast_example" + ":/data/ biocontainers/blast:v2.2.31_cv2 blastp -query P04156.fasta -db zebrafish.1.protein.faa -out results.txt")