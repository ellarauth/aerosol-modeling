#This R code allows one to compare models that are trained with all data and data from a certain city.

#The data are processed with months.py to obtain season variable z.
data <- read.csv('merged2.csv')

for (i in 1:length(data$X)){  ## Values for season are multiplied with -1 in the Southern Hemisphere.
  if (data$latitude[i]<0){
    data$z[i]=-data$z[i]
  }
}

rmse = function(m, o){
  sqrt(mean((m - o)^2))
}

city <- 'VAR'  # Choose the city for model comparison.

smp_size <- floor(0.75 * nrow(data))   #Constructing a random sample from the data
set.seed(123)
train_ind <- sample(seq_len(nrow(data)), size = smp_size)

train2 <- data[train_ind, ]  # Training set for global model
test <- data[-train_ind, ]
test <- test[test$city==city,]

train=train2[train2$city==city,] # Training set for local model

m <- lm(concentration~I(exp(0.01*t))+log(co)+t+z+so2, data=train)  # Train local model
m2 <- lm(concentration~I(exp(0.01*t))+log(co)+t+so2, data=train2)  # Train global model
summary(m)
summary(m2)

prediction <- predict(m, test) # Predict the concentration for test set with local model

for (i in 1:length((prediction))){  # Predicted values under zero are set to zero.
  if (prediction[i]<0){
    prediction[i] <- 0
  }
}

prediction2 <- predict(m2, test) # Predict the concentration for test set with global model

for (i in 1:length((prediction2))){  # Predicted values under zero are set to zero.
  if (prediction2[i]<0){
    prediction2[i] <- 0
  }
}

par(mfrow=c(2,1))   # The models are plotted for visual inspection.
plot(test$concentration, type='l', col='red', main=city, xlab = 'time', ylab = 'n100', sub = 'local model')
lines(prediction, col='blue')
legend("topleft", legend=c('measured (red)','prediction (blue)'))
legend("topright", legend=c('RMSE',rmse(prediction,test$concentration)))
plot(test$concentration, type='l', col='red', main=city, xlab = 'time', ylab = 'n100', sub = 'global model')
lines(prediction2, col='blue')
legend("topleft", legend=c('measured (red)','prediction (blue)'))
legend("topright", legend=c('RMSE',rmse(prediction2,test$concentration)))







