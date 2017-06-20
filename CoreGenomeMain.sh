#!/bin/sh

#make new fasta
./MkCoreGenome.py hglft_Gene.bed /home/UCSC/Sequences/hg38.fa ./Newhg/Newhg38.fa

#build bwa index
bwa index ./Newhg/Newhg38.fa

fastaindex="Newhg/Newhg38.fa"
fastq1="TestFq/Amplicon5-8-13_C8YYGANXX_L3_1.clean.fq.gz"
fastq2="TestFq/Amplicon5-8-13_C8YYGANXX_L3_2.clean.fq.gz"
Generegion="hglft_Gene.bed"
chromsize="hg38.chrom.sizes"
bamfile="TestFq/Amplicon.bam"


#map fastaq to Newfasta
bwa mem -t 20 -M $fastaindex $fastq1 $fastq2 > tmp1.sam

#transform old sam to sam with right chromosome and postion
./MapCoreGenome.py $Generegion tmp1.sam $chromsize tmp2.sam

#sam to bam
samtools view -bS tmp2.sam > $bamfile

rm tmp1.sam tmp2.sam
