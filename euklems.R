library(MASS)
library(reshape)
library(reshape2)
library(stringr)
library(tidyr)
library(data.table)

data=read.csv('C:/Users/macbook/Desktop/RA/emp data/original data/euklems.csv')

##filter the industry
data1 <- subset(data, nace_r2_code=="A"|nace_r2_code=="B"|nace_r2_code=="C"|nace_r2_code=="D-E"|nace_r2_code=="F"|nace_r2_code=="G"|nace_r2_code=="H"|nace_r2_code=="I"|nace_r2_code=="J"|nace_r2_code=="K"|nace_r2_code=="L"|nace_r2_code=="M-N"|nace_r2_code=="O-Q"|nace_r2_code=="R-S"|nace_r2_code=="T"|nace_r2_code=="U")

##choose the variable
data2 <- data1[, c("geo_name", "geo_code", "year","nace_r2_code","EMP")]

## transform the data
setDT(data2)
data3 <- dcast(data2, geo_name + geo_code +year  ~ nace_r2_code, fun.aggregate = NULL, value.var='EMP')

## As U is small and always miss, change NA of U to 0
data3$U <- ifelse(is.na(data3$"U"), 0, data3$U)

## drop EU data
data4 <- subset(data3, nchar(geo_code)==2)

## drop imcomplete record
data4 <- data4[complete.cases(data4), ]
data4$Trade <- rowSums(data4[,c("G","I")])
data4$Transport <- rowSums(data4[,c("H","J")])
data4$Business <- rowSums(data4[,c("K","L","M-N")])
data4$Others <- rowSums(data4[,c("R-S","T","U")])

##rename
data4$Country <-data4$geo_name
data4$Agriculture <-  data4$A 
data4$Mining <-  data4$B 
data4$Manufacturing <-  data4$C 
data4$Utilities <-  data4$"D-E" 
data4$Construction  <-  data4$F 
data4$Government <-  data4$"O-Q"
data5 <- data4[,c("Country","geo_code","year","Agriculture","Mining","Manufacturing","Utilities","Construction","Trade","Transport","Business","Government","Others")]
##export
write.csv(data5,"C:/Users/macbook/Desktop/RA/emp data/result data/neweuklems.csv")

