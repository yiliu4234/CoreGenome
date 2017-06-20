library(data.table)

amplicon <- fread("/home/ywliao/project/Gengyan/amplicon_primer.txt") # 
GeneAnno <- fread("/home/ywliao/utilities/UCSC/hg19annotation",skip = 1,col.names = c("Chr","Start","End","KgID","Gene","Description"))
setkey(GeneAnno,Chr,Start,End,Gene)
Gene.bed <- GeneAnno[amplicon$Gene,.(Chr,Start,End,Gene),on="Gene",mult="last"]
fwrite(Gene.bed,file="/home/ywliao/project/Gengyan/GeneRegion.bed",sep="\t",col.names = F)
