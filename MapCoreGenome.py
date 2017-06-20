#!/usr/bin/python
import sys

def MkGeneDic(bedfile):
    '''
    save Gene as key,its Chr and Start as value

    Args:
      bedfile: bed format;Chr Start End Gene
    Return:
      GeneDic: [chr1:(start,end)]

    '''
    f = open(bedfile,'r')
    GeneDic={}
    for eachline in f:
       lst=eachline.strip().split("\t")
       Chr=lst[0]
       Start=int(lst[1])
       End=int(lst[2])
       Gene=lst[3]
       GeneDic[Gene]=(Chr,Start)
    f.close()
    return GeneDic

def WtSQ(chromsize,GeneDic,outfile):
    '''
    write SQ header
  
    Args:
      chromsize: chromsize file
      GeneDic: {Gene:(Chr,length of the chr)...}
      outfile: new sam file object to write

    '''
    ChrSet=set()
    for Gene in GeneDic:
        ChrSet.add(GeneDic[Gene][0])
    f=open(chromsize,'r')
    for eachline in f:
        lst=eachline.strip().split("\t")
        Chr=lst[0]
        length=int(lst[1])
        if Chr in ChrSet:
            outfile.write("@SQ\tSN:%s\tLN:%d\n" % (Chr,length))
    f.close()

    
if len(sys.argv) == 5:
    bedfile=sys.argv[1]
    oldsam=sys.argv[2]
    chromsize=sys.argv[3]
    newsam=sys.argv[4]
else:
    print("[usage] "+ sys.argv[0]+" GeneRegion.bed oldsam chromsize newsam")
    print("      bedfile: Chr Start End Gene(four columns are neccesary)...,seperated by tab,should be sorted by Chr")
    print("      oldsam: a sam file generated by mapping to Core fasta genome")
    print("      chormsize: choomrsize file,ex: Chr1\t249250621,seperated by tab")
    print("Output: a new sam file with right chromatosome and postition")
    sys.exit(-1)



GeneDic=MkGeneDic(bedfile)
outfile=open(newsam,'w+')
infile=open(oldsam,'r')
SQ=bool(1)
for eachline in infile:
    if eachline.startswith("@"):
        if eachline.startswith("@SQ"):
            if SQ:
                SQ=bool(0)
                WtSQ(chromsize,GeneDic,outfile)
            else:
                pass
        else:
            outfile.write(eachline)
    else:
        lst=eachline.strip().split("\t")
        RNAME=lst[2]
        Gene=RNAME
        POS=int(lst[3])
        RNEXT=lst[6]
        PNEXT=int(lst[7])
        if RNAME != "*":
            POS=GeneDic[Gene][1]+POS-100
            RNAME=GeneDic[Gene][0]
            if RNEXT == "=":
                PNEXT=GeneDic[Gene][1]+PNEXT-100
            elif RNEXT == "*":
                pass
            else:
                RNEXT=GeneDic[Gene][0]
                PNEXT=GeneDic[Gene][1]+PNEXT-100
            outfile.write("%s\t%d\t%s\t%d\t%d\t%s\t%s\t%d\t%d\t%s\n" % (lst[0],int(lst[1]),RNAME,POS,int(lst[4]),lst[5],RNEXT,PNEXT,int(lst[8]),"\t".join(lst[9:len(lst)]))) 
        else:
            outfile.write(eachline)     
outfile.close()
