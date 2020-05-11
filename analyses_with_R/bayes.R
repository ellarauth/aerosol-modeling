#Bayesian regression model using Stan

library(ggplot2)
library(StanHeaders)
library(rstan)
library(coda)
options(mc.cores = parallel::detectCores())
rstan_options(auto_write = TRUE)

data <- read.csv('merged.csv')

city <- 'MAR'    # choose city
test <- data[data$city==city,]
train <- data[data$city==city,]


smp_size <- floor(0.75*nrow(test))   # construct a random sample for training set
set.seed(123)
train_ind <- sample(seq_len(nrow(test)),size = smp_size)
train <- test[train_ind,]
test <- test[-train_ind,]

# variables used
y <- train$concentration
t <- train$t
co <- train$co
z <- train$z

# model definition

model = "
  data{
  int<lower=0> N; // number of observations
  real y[N];
  real t[N];
  real z[N];
  real co[N];

}
parameters{
  real a;
  real b;
  real c;
  real d;
  real e;
  real<lower=0> sigma2;
}
transformed parameters{
  real<lower=0> sigma;
  real mu[N];
  sigma=sqrt(sigma2);
  for( i in 1 : N ) {
    mu[i] = a + b * exp(0.01*t[i]) + c * log(co[i]) + d * t[i] + e * z[i];
  }
}
model{
  a ~ normal( 0, sqrt(1e6));
  b ~ normal( 0, sqrt(1e6));
  c ~ normal( 0, sqrt(1e6));
  d ~ normal( 0, sqrt(1e6));
  e ~ normal( 0, sqrt(1e6));
  sigma2 ~ inv_gamma(0.001,0.001);
  for( i in 1 : N ) {
    y[i] ~ normal(mu[i],sigma);
  }
}"

dat <- list (N=length(y), y=y, t=t, z=z, co=co) #define the data for the model

init1 <- list (a = 5, b = -10, c = 0,  sigma2 = 0.1) # initial values for parameters
init2 <- list (a = 0, b = -5, c = 10, sigma2 = 0.2)
init3 <- list (a = -5, b = 5, c = -5, sigma2 = 0.3)
init4 <- list (a = 10, b = 10, c = 5, sigma2 = 0.4)
inits <- list(init1, init2, init3,init4)


post=stan(model_code=model,data=dat,warmup=500,iter=2000,init=inits,chains=4,thin=1)

#calculate the posterior
plot(post,plotfun="trace", pars=c("a","b","c","d","e","sigma2"),inc_warmup=TRUE)

# check for autocorrelation
stan_ac(post,inc_warmup=FALSE,lags=25)

# take some values out of post
post_samples=as.matrix(post,pars=c("a","b","c","d","e","sigma2"))

# plot some distributions
par(mfrow=c(1,3))
hist(y,main='Measured observations',breaks=30)
hist(post_samples[,"a"],main="Posterior for a",xlab="a",breaks=30)
hist(post_samples[,"sigma2"],main="Posterior for sigma2",xlab="sigma2",breaks=30)


#create matrices needed for constructing predictive distribution
mu=matrix(NA,length(test$X),length(post_samples[,2]))
y.tilde=matrix(NA,length(test$X),length(post_samples[,2]))

mean_mu=rep(NA, length(test$X))
int_mu=matrix(NA, length(test$X),2)

mean_y=rep(NA, length(test$X))
int_y=matrix(NA, length(test$X),2)

#construct predictive distribution
for (i in 1:length(test$X)){
  mu[i,]=post_samples[,1]+post_samples[,2]*exp(0.01*t[i])+post_samples[,3]*log(co[i])+post_samples[,4]*t[i]+post_samples[,5]
  mean_mu[i]=mean(mu[i,])
  int_mu[i,]=quantile(mu[i,],probs = c(0.025,0.975),na.rm=T)
  
  y.tilde[i,]=mu[i,]+rnorm(length(mu[i,]),0,sqrt(post_samples[,6]))
  mean_y[i]=mean(y.tilde[i,])
  int_y[i,]=quantile(y.tilde[i,],probs = c(0.025,0.975),na.rm = T)
}
par(mfrow=c(1,1))
plot(mean_mu,type="l",col="blue")
#lines(int_mu[,1],col="green")
#lines(int_mu[,2],col="green")
lines(mean_y,type="l",col="magenta")  #plot prediction
lines(int_y[,1],col="red")            #plot 95% quantile for prediction
lines(int_y[,2],col="red")
lines(test$concentration)             #plot measured values
points(test$concentration,cex=0.2)


rmse <- function(m,o){
  sqrt(mean(m-0)^2)
}

rmse(mean_y,y)

par(mfrow=c(1,2))   #compare predictive distribution and measured values
hist(y.tilde, breaks = 30)
hist(y, breaks = 30)


