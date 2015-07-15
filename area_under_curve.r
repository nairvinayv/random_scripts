#Code for calculating the area under curve using Trapezoidal Integration
#Input File has single column containing Values


args <- commandArgs(trailingOnly = TRUE);
raw_data = read.csv(args[1])
data <- cbind(1:dim(raw_data)[1],raw_data)
require(pracma)
AUC = trapz(as.vector(t(data[1])),as.vector(t(data[2])))
disp(AUC)
