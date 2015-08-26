#R-Code for generating Polar plots using the plotrix library
library(plotrix)
data<-read.csv('15T-epsilon.dat')

setEPS()
png("15T-epsilon.png")
polar.plot(data[1:14999,1],data[1:14999,2],rp.type="p",start=90,clockwise=TRUE,main=expression(paste("Torsion Angles: 1,5T-",epsilon)))
dev.off()
