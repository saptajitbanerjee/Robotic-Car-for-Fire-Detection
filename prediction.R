data = read.csv("C:\\Users\\aqibk\\Downloads\\fire.csv", stringsAsFactors = FALSE)
train_data = data.frame(Temperature = c(data$temp), Humidity=c(data$RH), ISI=c(data$ISI))
model = lm(train_data$ISI~train_data$Temperature+train_data$Humidity, data=train_data)
summary(model)
library(gsheet)
test_data = gsheet2tbl('https://docs.google.com/spreadsheets/d/1yZwcWqGl8_3GYGyUQPb0dN59mDFAj05FJdZ8sEv-2Fk/edit#gid=0')
coeff = coef(model)
for (i in 1:nrow(test_data)){
  temp = data.frame(x=c(test_data[i,3]), y=c(test_data[i,4]))
  res = coeff[1]+temp[,1]*coeff[2]+temp[,2]*coeff[3]
  print(paste("Temperature: ",temp[,1]," Humidity: ",temp[,2]," Predicted: ",round(res,1)))
}
