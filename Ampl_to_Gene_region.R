────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#!/bin/Rscript

library(data.table)

arg <- commandArgs(T)
if (length(arg) != 3) {
    message("[usage]: Ampl_to_Gene_region.R bedfile gtffile outputfile")
    message("    bedfile format: chr start end information(Arbitrary but can not be lacked)")
    message("    GTFfile: gtf file downloaded from GENCODE")
    message("    outputfile: gene region file to be writen out")
    message("    needed package: data.table 1.10.4")
    stop("Please check your arguments!")
}
bedfile <- arg[1]
annofile <- arg[2]
outfile <- arg[3]

#read file 
bed <- fread(bedfile,sep="\t") #
anno <- fread(annofile,sep="\t") #Download from GENCODE
setnames(anno,c("V1","V2","V3","V4","V5","V9"),c("Chr","Gene","Type","Start","End","Info"))
anno <- anno[Type=="gene",.(Chr,Start,End,Gene=sapply(strsplit(tstrsplit(Info,";")[3][[1]],"\""),function(x)x[2]))]
setkey(anno,Chr,Start,End)
setkey(bed,V1,V2,V3)

#find overlaps by Chr
lst <- list()
for (ChrI in intersect(unique(bed$V1),unique(anno$Chr))){
  anno_reg <- anno[Chr == ChrI,.(Start,End)]
  bed_reg <- bed[V1 == ChrI,.(V2,V3)]
  setkey(anno_reg,Start,End)
  setkey(bed_reg,V2,V3)
  overl <- foverlaps(bed_reg,anno_reg,which=TRUE,nomatch = 0)
  if (nrow(overl) > 0){
    lst[[ChrI]] <- data.table(Chr=ChrI,bed[V1 == ChrI,][overl[["xid"]],.(V2,V3,V4)],anno[Chr == ChrI][overl[["yid"]],.(Gene,GeneStart=Start,GeneEnd=End)])
  }
}
merge_dt <- rbindlist(lst)
setnames(merge_dt,c("V2","V3","V4"),c("Start","End","Name"))
merge_dt <- unique(merge_dt[,.(Chr,GeneStart,GeneEnd,Gene)])
fwrite(merge_dt,outfile,sep="\t",col.names = F)



