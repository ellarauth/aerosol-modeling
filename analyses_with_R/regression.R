#This R code allows one to experiment with different linear models and compare them.

#The data are processed with months.py to obtain season variable z.
data <- read.csv('merged2.csv')

for (i in 1:length(data$X)){  # Values for season are multiplied with -1 in the Southern Hemisphere.
  if (data$latitude[i]<0){
    data$z[i]=-data$z[i]
  }
}

rmse <-  function(m, o){
  sqrt(mean((m - o)^2))
}

city <- 'HYY'   # Choose the city
test <- data[data$city==city,]  # By using just test <- data and train <- data it is
train <- data[data$city==city,]  # possible to use the whole dataset, that is, all the cities.

#raja <- floor(nrow(test)*3/4)     # non-random sample
#test=test[(raja+1):length(test$X),]
#train=train[1:raja,]

smp_size <- floor(0.75 * nrow(test))   # size of training data
set.seed(123)
train_ind <- sample(seq_len(nrow(test)), size = smp_size)  # indices for random sample

train <- test[train_ind, ]  # The data is divided into test und train sets
test <- test[-train_ind, ]


m <- lm(concentration~I(exp(0.01*t))+log(co)+t+z+so2, data=train)   # Two models are trained so that they can be compared.
m2 <- lm(concentration~I(exp(0.01*t))+log(co)+t+z+no+no2+so2+c5h8, data=train)
summary(m)
summary(m2)


prediction <- predict(m, test)  # Predict the concentration for test set

for (i in 1:length((prediction))){   # Predicted values under zero are set to zero.
  if (prediction[i]<0){
    prediction[i] <- 0
  }
}

prediction2 <- predict(m2, test)

for (i in 1:length((prediction2))){
  if (prediction2[i]<0){
    prediction2[i] <- 0
  }
}

summary(prediction)   # Compare mean, median, and quantiles of predictions to the real values
summary(prediction2)
summary(test$concentration)

rmse(prediction,test$concentration)
rmse(prediction2,test$concentration)

par(mfrow=c(2,1))
plot(test$concentration, type='l', col='red', main=city)   # Plot real values and prediction to same
lines(prediction, col='blue')                                # figure for visual evaluation.
plot(test$concentration, type='l', col='red', main=city)
lines(prediction2, col='blue')
#lines((test$t-273)*10+500, col='green')  # Possibility to plot t and co to the same figure (not in scale)
#lines(test$co*10000000000, col='orange')

#plot(m)     # Plots of residuals etc.

#plot(test$date, test$concentration, type='l',col='red')
#lines(test$date, prediction, col='blue')


