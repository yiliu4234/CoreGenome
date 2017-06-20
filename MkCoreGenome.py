#!/usr/bin/python
import sys

def MkDic(fafile):
    '''
    Devide fasta file into chroms, and save to FaDic
    '''
    FaDic={}
    f=open(fafile,'r')
    for eachline in f:
        if eachline.startswith(">"):
            Chr=eachline.strip()
            FaDic[Chr]=[]
        else:
            FaDic[Chr].extend(list(eachline.strip()))
    f.close()
    return FaDic

    
if len(sys.argv) == 4:
    bedfile=sys.argv[1]
    fafile=sys.argv[2]
else:
    print("[usage] "+ sys.argv[0]+" bedfile fafile outputfile")
    print("Tips: bedfile:Chr Start End ,or Chr Start End ...,seperated by tab,should be sorted by Chr")
    print("       fafile: Reference Genome")
    print("Output: a new fasta file, it only has bed region +-100 bp sequence")
    sys.exit(-1)


Fadic=MkDic(fafile)
f = open(bedfile,'r')
CurChr=""
NewFadic={}
outFa=""
for eachline in f:
   lst=eachline.strip().split("\t")
   Chr=lst[0]
   Start=int(lst[1])
   End=int(lst[2])
   Gene=lst[3]
   if Chr != CurChr:
       CurChr=Chr
       if ">"+CurChr in Fadic:
           faseqlst=Fadic[">"+CurChr]
       #else:
          #print "Error ! "+CurChr+" not eixsts in fasta file!" 
   if ">"+CurChr in Fadic:
       seq=faseqlst[Start-100:End+100]
       NewFadic[Gene]=seq
f.close()

#write new fasta to outputfile
outfile=open(sys.argv[3],'w+')
for Gene in NewFadic:
    outFa=NewFadic[Gene]
    outfile.write(">"+Gene+"\n")
    for Line in (outFa[i:i+50] for i in xrange(0,len(outFa),50)):
        outfile.write(''.join(Line)+"\n")
outfile.close()
