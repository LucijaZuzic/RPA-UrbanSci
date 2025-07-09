# Clear environment
rm(list=ls())
library(fNonlinear)
library(crqa)

## The R script for Filjar et al manuscript prepared for MDPI Urban Science

# Set path to the working directory containing prepared data set

library(tidyverse)
getCurrentFileLocation <-  function()
{
  this_file <- commandArgs() %>% 
    tibble::enframe(name = NULL) %>%
    tidyr::separate(col = value, into = c("key", "value"), sep = "=", fill = 'right') %>%
    dplyr::filter(key == "--file") %>%
    dplyr::pull(value)
  if (length(this_file) == 0) {
    this_file <- rstudioapi::getSourceEditorContext()$path
  }
  return(dirname(this_file))
}

# set parameters for RPA plots (same for all plots)
delay = 1
embed = 1
rescale = 1
radius = 1
normalize = 0
mindiagline = 2
minvertline = 2
tw = 0
whiteline = FALSE
recpt = FALSE
side = "both"
checkl = list(do = FALSE, thrshd = 3, datatype = "categorical", pad = TRUE)
par = list(unit = 2, labelx = "Time", labely = "Time", cols = "red", pcex = 1)

# Sin function
x <- seq(-500, 500, by = 1/1)
y =sin(x)
ts_y <- as.ts(y)
dataframe_sin <- data.frame(ts_y)
colnames(dataframe_sin) <- c("sin")
write.csv(dataframe_sin, "sin_time_series.csv", row.names = FALSE)

# Normal distribution - white noise
y = rnorm(1000)
ts_y <- as.ts(y)
dataframe_normal <- data.frame(ts_y)
colnames(dataframe_normal) <- c("normal")
write.csv(dataframe_normal, "normal_time_series.csv", row.names = FALSE)

# Auto-regressive time sequence
alpha = -0.99
# purely random process
Z <- rnorm(1000, mean = 0, sd = 0.5)
# seed
X <- rnorm(1)
# the process
for (i in 2:length(Z)) {
  X[i] <- alpha*X[i-1]+Z[i]
}
ts_y <- as.ts(X)
dataframe_ar <- data.frame(ts_y)
colnames(dataframe_ar) <- c("ar")
write.csv(dataframe_ar, "ar_time_series.csv", row.names = FALSE)

# Brownian motion
t <- 0:(1000)  # time
sig2 <- 0.01
## first, simulate a set of random deviates
x <- rnorm(n = length(t) - 1, sd = sqrt(sig2))
## now compute their cumulative sum
x <- c(0, cumsum(x))
ts_y <- as.ts(x)
dataframe_brownian <- data.frame(ts_y)
colnames(dataframe_brownian) <- c("brownian")
write.csv(dataframe_brownian, "brownian_time_series.csv", row.names = FALSE)

# Logistic map
logistic.map <- function(r, x, N, M){
  ## r: bifurcation parameter
  ## x: initial value
  ## N: number of iteration
  ## M: number of iteration points to be returned
  z <- 1:N
  z[1] <- x
  for(i in c(1:(N-1))){
    z[i+1] <- r *z[i]  * (1 - z[i])
  }
  ## Return the last M iterations 
  z[c((N-M):N)]
}

library(compiler) ## requires R >= 2.13.0
logistic.map <- cmpfun(logistic.map) # same function as above
lm<-logistic.map(3.56995, 0.01, 1000, 400)
ts_y <- as.ts(lm)
dataframe_logistic <- data.frame(ts_y)
colnames(dataframe_logistic) <- c("logistic")
write.csv(dataframe_logistic, "logistic_time_series.csv", row.names = FALSE)