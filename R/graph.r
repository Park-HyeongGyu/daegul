library(ggplot2)
library(dplyr)

seoul <- read.csv('./data/seoul.csv')
busan <- read.csv('./data/busan.csv')
ulsan <- read.csv('./data/ulsan.csv')
daegu <- read.csv("./data/daegu.csv")
gwangju <- read.csv("./data/gwangju.csv")
incheon <- read.csv("./data/incheon.csv")
daejeon <- read.csv("./data/daejeon.csv")

seoul$type <- factor(seoul$type)
busan$type <- factor(busan$type)
ulsan$type <- factor(ulsan$type)
daegu$type <- factor(daegu$type)
gwangju$type <- factor(gwangju$type)
incheon$type <- factor(incheon$type)
daejeon$type <- factor(daejeon$type)

#seoul outlier 제거
#https://www.r-bloggers.com/2020/01/how-to-remove-outliers-in-r/
lib <- subset(seoul, type == "library")
outliars_lib <- boxplot(lib$nearest_distance, plot=FALSE)$out
lib <- lib[-which(lib$nearest_distance %in% outliars_lib),]
theater <- subset(seoul, type == "theater")
outliars_theater <- boxplot(theater$nearest_distance, plot=FALSE)$out
theater <- theater[-which(theater$nearest_distance %in% outliars_theater),]
gym <- subset(seoul, type == "gym")
outliars_gym <- boxplot(gym$nearest_distance, plot=FALSE)$out
gym <- gym[-which(gym$nearest_distance %in% outliars_gym),]
seoul_n <- rbind(lib, theater, gym)

#daejeon outlier 제거
#https://www.r-bloggers.com/2020/01/how-to-remove-outliers-in-r/
lib <- subset(daejeon, type == "library")
outliars_lib <- boxplot(lib$nearest_distance, plot=FALSE)$out
lib <- lib[-which(lib$nearest_distance %in% outliars_lib),]
theater <- subset(daejeon, type == "theater")
outliars_theater <- boxplot(theater$nearest_distance, plot=FALSE)$out
theater <- theater[-which(theater$nearest_distance %in% outliars_theater),]
gym <- subset(daejeon, type == "gym")
outliars_gym <- boxplot(gym$nearest_distance, plot=FALSE)$out
gym <- gym[-which(gym$nearest_distance %in% outliars_gym),]
daejeon_n <- rbind(lib, theater, gym)

#gwangju outlier 제거
#https://www.r-bloggers.com/2020/01/how-to-remove-outliers-in-r/
lib <- subset(gwangju, type == "library")
outliars_lib <- boxplot(lib$nearest_distance, plot=FALSE)$out
lib <- lib[-which(lib$nearest_distance %in% outliars_lib),]
theater <- subset(gwangju, type == "theater")
outliars_theater <- boxplot(theater$nearest_distance, plot=FALSE)$out
theater <- theater[-which(theater$nearest_distance %in% outliars_theater),]
gym <- subset(gwangju, type == "gym")
outliars_gym <- boxplot(gym$nearest_distance, plot=FALSE)$out
gym <- gym[-which(gym$nearest_distance %in% outliars_gym),]
gwangju_n <- rbind(lib, theater, gym)

#busan outlier 제거
#https://www.r-bloggers.com/2020/01/how-to-remove-outliers-in-r/
lib <- subset(busan, type == "library")
outliars_lib <- boxplot(lib$nearest_distance, plot=FALSE)$out
lib <- lib[-which(lib$nearest_distance %in% outliars_lib),]
theater <- subset(busan, type == "theater")
outliars_theater <- boxplot(theater$nearest_distance, plot=FALSE)$out
theater <- theater[-which(theater$nearest_distance %in% outliars_theater),]
gym <- subset(busan, type == "gym")
outliars_gym <- boxplot(gym$nearest_distance, plot=FALSE)$out
gym <- gym[-which(gym$nearest_distance %in% outliars_gym),]
busan_n <- rbind(lib, theater, gym)

# 서울의 데이터
ggplot(seoul_n, aes(x=nearest_distance, fill=type)) +
  geom_histogram(binwidth = 100, position="identity", alpha=0.8)
head(data)

ggplot(seoul_n, aes(x=nearest_distance)) +
  geom_histogram(binwidth =100, fill="white", colour="black") +
  facet_grid(type ~ ., scales="free")

ggplot(gwangju_n, aes(x=nearest_distance)) +
  geom_histogram(binwidth =100, fill="white", colour="black") +
  facet_grid(type ~ ., scales="free")

ggplot(daejeon_n, aes(x=nearest_distance)) +
  geom_histogram(binwidth =100, fill="white", colour="black") +
  facet_grid(type ~ ., scales="free")

ggplot(busan_n, aes(x=nearest_distance)) +
  geom_histogram(binwidth =200, fill="white", colour="black") +
  facet_grid(type ~ ., scales="free")




summary(seoul[seoul$type == "library",])

#상관관계분석

seoul_lib <- mean(seoul[seoul$type == "library",]$nearest_distance)
gwangju_lib <- mean(gwangju_n[gwangju_n$type == "library",]$nearest_distance)
daegu_lib <- mean(daegu[daegu$type == "library",]$nearest_distance)
incheon_lib <- mean(incheon[incheon$type == "library",]$nearest_distance)
daejeon_lib <- mean(daejeon[daejeon$type == "library",]$nearest_distance)
busan_lib <- mean(busan[busan$type == "library",]$nearest_distance)
ulsan_lib <- mean(ulsan[ulsan$type == "library",]$nearest_distance)

index <- read.csv('./data/index_by_city.csv')
index[, 'distance'] = c(seoul_lib, busan_lib, daegu_lib, incheon_lib, 
                        gwangju_lib, daejeon_lib, ulsan_lib)
plot(index$annual_rate, index$distance)
