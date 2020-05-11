# This script determines the best value for b in exp(b*t). This script should be used with the other scripts as well to obtain a good value for b.
data <- read.csv('merged2.csv')

for (i in 1:length(data$X)){  # Values for season are multiplied with -1 in the Southern Hemisphere. months.py does not do this.
  if (data$latitude[i]<0){
    data$z[i]=-data$z[i]
  }
}

rmse <-  function(m, o){
  sqrt(mean((m - o)^2))
}


smp_size <- floor(0.75 * nrow(data))   #Constructing a random sample from the data
set.seed(123)
train_ind <- sample(seq_len(nrow(data)), size = smp_size)

train <- data[train_ind, ]  # Training and testing sets
test <- data[-train_ind, ]

#city <- 'HYY'     # Possibility to use data from a single location
#train <- train[train$city==city,]
#test <- test[test$city==city,]


d <- 10000   # some large number as initial RMSE value
a <- seq(0.001,1,by=0.001)  # candidate values for b


for (b in a){    # This loop tries different values for b. It stops when RMSE starts growing.
  m <- lm(concentration~I(exp(b*t))+t+log(co)+co+no2+so2+c5h8, data=train)
  prediction <- predict(m, test) # Predict the concentration for test set
  
  for (i in 1:length((prediction))){  # Predicted values under zero are set to zero.
    if (prediction[i]<0){
      prediction[i] <- 0
    }
  }
  c <- rmse(prediction,test$concentration)

  if (c>d){     # If new RMSE value is larger than the best one (previous), the loop stops.
    break
  }
  d <- c   # The smallest RMSE is saved.
  g <- b   # The best value for b is saved.
  print(g)
  print(c)
}

print(g)


m <- lm(concentration~I(exp(g*t))+t+log(co)+co+no2+so2+c5h8, data=train)   # Fitting the model. Saving the best model in the loop caused some problems,
summary(m)                                                                 # so the model must be fitted again.

prediction2 <- predict(m, test) # Predict the concentration for test set
summary(prediction2)

for (i in 1:length((prediction2))){  # Predicted values under zero are set to zero.
  if (prediction2[i]<0){
    prediction2[i] <- 0
  }
}
rmse(prediction2,test$concentration)

plot(prediction2,test$concentration, log = 'xy', ylab = 'measured', xlab = 'predicted') #Plotting predicted value vs. measured value
lines(c(1:10000),c(1:10000), col='red')    # Line that denotes the perfect fit

par(mfrow=c(1,1))
plot(test$concentration, type='l', col='red', main='ALL', xlab = 'time', ylab = 'n100', log = 'y')   # Plot measured values and prediction to same plot
lines(prediction2, col='blue')
legend("topleft", legend=c('measured (red)','prediction (blue)'))
legend("topright", legend=c('RMSE',rmse(prediction2,test$concentration)))
#lines((test$t-273)*10+500, col='green')  # Possibility to plot t and co to the same figure (not in scale)
#lines(test$co*10000000000, col='orange')
