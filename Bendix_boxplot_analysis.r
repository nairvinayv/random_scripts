#Code for analysing data from Bendix Plugin of VMD
#List of Files
inp_list = c("S6_A","S6_B","S6_C","S6_D")
data=list()

#Reading in the files and storing the data in a list of lists
for(i in 1:4)
{
	file_id = sprintf("%s_data",inp_list[i])
	data[i] = list(read.csv(file_id, sep = '\t', header = FALSE))
}
residues = readLines('S6_rownames')

#Boxplot of helix curvature of each chain plotted onto same graph
setEPS()
postscript("S6_curvature.eps")
for(i in 1:4)
{
	boxplot(data[[i]],col=i+1,ylim=c(0,100),xlab="Residue Number",ylab="Curvature",main="Helicity of S6 Helix",xaxt = 'n')
	par(new=TRUE)
}
text(x =  seq_along(residues), y = par("usr")[3] - 1, srt = 90, adj = 1, labels = residues, xpd = TRUE)
legend(32.5, 101, c("A Chain","B Chain","C Chain","D Chain"),col=c(2,3,4,5),lty=c(1,1),lwd=c(2.5,2.5))
dev.off()

#Individual Heatmaps of each chain 
for(i in 1:4)
{
	plot.new()
	frame()
	setEPS()
	out_file = sprintf("heatmap_%s.eps",inp_list[i])
	postscript(out_file)
	datamatrix <-as.matrix(data[[i]],headers = FALSE)
	cc <- rainbow(ncol(datamatrix), start = 0, end = 0.5)
	frames <- rep("", nrow(datamatrix))
	frames[seq(1,nrow(datamatrix), 100)] <- seq(1, nrow(datamatrix), 100)
	heatmap(datamatrix,Rowv = NA, Colv = NA, scale = "row",xlab = "S6 Helix Residue", ylab =  "Time",col = cc, ColSideColors = cc,labCol = residues,labRow = frames, cexRow=2,cexCol=1)
	dev.off()
}
