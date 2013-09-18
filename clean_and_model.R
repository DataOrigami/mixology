Sys.setlocale(locale="C")
setwd("~/Dropbox//Nick's Work//Data Origami//")
data_uncleaned <- read.csv("6K.csv", header=FALSE)
colnames(data_uncleaned) <- c('id','name','rating','votes','ing1','ing2','ing3','ing4','ing5','ing6')
for(i in 5:10) {
  col <- as.character(data_uncleaned[,i])
  col <- gsub('[0-9]+', '', col)
  col <- gsub('tsp', '', col)
  col <- gsub('tblsp', '', col)
  col <- gsub('shots', '', col)
  col <- gsub('shot', '', col)
  col <- gsub('splash', '', col)
  col <- gsub('small', '', col)
  col <- gsub('scoops', '', col)
  col <- gsub('scoop', '', col)
  col <- gsub('sticks', '', col)
  col <- gsub('pint', '', col)
  col <- gsub('parts', '', col)
  col <- gsub('part', '', col)
  col <- gsub('pieces', '', col)
  col <- gsub('piece', '', col)
  col <- gsub('pinches', '', col)
  col <- gsub('pinch', '', col)
  col <- gsub('bottles', '', col)
  col <- gsub('bottle', '', col)
  col <- gsub('bags', '', col)
  col <- gsub('bag', '', col)
  col <- gsub('cans', '', col)
  col <- gsub('chunks', '', col)
  col <- gsub('chunk', '', col)
  col <- gsub('cheap', '', col)
  col <- gsub('chopped', '', col)
  col <- gsub('clear', '', col)
  col <- gsub('cups', '', col)
  col <- gsub('cup', '', col)
  col <- gsub('cubes', '', col)
  col <- gsub('cube', '', col)
  col <- gsub('shot', '', col)
  col <- gsub('dashes', '', col)
  col <- gsub('dash', '', col)
  col <- gsub('fifth', '', col)
  col <- gsub('drop', '', col)
  col <- gsub('fresh', '', col)
  col <- gsub('gal', '', col)
  col <- gsub('glasses', '', col)
  col <- gsub('glass', '', col)
  col <- gsub('jigger', '', col)
  col <- gsub('inch', '', col)
  col <- gsub('instant', '', col)
  col <- gsub('large', '', col)
  col <- gsub('measure', '', col)
  col <- gsub('oz', '', col)
  col <- gsub('lb', '', col)
  col <- gsub('cl', '', col)
  col <- gsub('ml', '', col)
  col <- gsub('qt', '', col)
  col <- gsub('dl', '', col)
  col <- gsub(' +', '', col)
  col <- gsub('\\/', '', col)
  col <- gsub(',', '', col)
  col <- gsub('-', '', col)
  data_uncleaned[,i] <- factor(col)
}

ing <- c()
for(i in 5:10) {
  ing <- c(ing,levels(data_uncleaned[,i]))
}
ing <- unique(ing)

cleaned <- matrix(numeric(0), nrow=nrow(data_uncleaned), ncol=length(ing))
cleaned <- cbind(cbind(as.matrix(as.numeric(data_uncleaned$rating)), as.matrix(as.numeric(data_uncleaned$votes))), cleaned)
for(i in 1:nrow(data_uncleaned)){
  print(i)
  for(k in 5:10) {
    cleaned[i,which(ing == data_uncleaned[i,k])] = 1
  }
}

cleaned[is.na(cleaned)] <- 0

cleaned<-as.data.frame(cleaned)
colnames(cleaned)<-c('ratings', 'votes', ing)

rating <- as.matrix(cleaned[,1])
votes <- 1/as.matrix(cleaned[,2])
ingredients <- as.matrix(cleaned[,3:(ncol(cleaned))])

model <- lm(rating ~ ingredients, weights=votes)

head(sort(model$coefficients, decreasing=TRUE), 20)

names_and_votes <- data_uncleaned[,c('name', 'rating', 'votes')]

transform_data <- function(x) {
  split_name <- t(t(unlist(strsplit(x['name'], split=' ', fixed=TRUE))))
  cbind(x['rating'], cbind(x['votes'], tolower(split_name)))
}

data <- apply(names_and_votes, 1, transform_data)
data <- do.call(rbind, data)
colnames(data) <- c('rating', 'votes', 'word')
row.names(data) <- NULL
data <- as.data.frame(data)
data$rating <- as.numeric(data$rating)
data$votes <- as.numeric(data$votes)
library(plyr)

counts <- ddply(data, .(word), summarize, count=length(word))
counts <- counts[counts$count > 5,]

data <- merge(data, counts, all.x=FALSE, all.y=FALSE)

model <- lm(rating ~ word, data=data, weights=(1/votes))

head(sort(model$coefficients, decreasing=TRUE), 10)