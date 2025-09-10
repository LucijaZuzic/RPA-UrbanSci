# Clear environment
rm(list=ls())
library(fNonlinear)
library(crqa)

## The R script for Zuzic et al manuscript prepared for MDPI Urban Science

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

setwd(getCurrentFileLocation())

# Logistic map with linear trend
logistic.map.linear.trend <- function(r, x, N, M, a){
  ## r: bifurcation parameter
  ## x: initial value
  ## N: number of iteration
  ## M: number of iteration points to be returned
  ## a: slope for the linear function to add
  z <- 1:N
  z[1] <- x
  for(i in c(1:(N-1))){
    z[i+1] <- r * z[i]  * (1 - z[i])
  }
  for(i in c(1:N)){
    z[i] <- z[i] + a * i
  }
  ## Return the last M iterations 
  z[c((N-M):N)]
}

library(compiler) ## requires R >= 2.13.0
logistic.map <- cmpfun(logistic.map.linear.trend) # same function as above
lm <- logistic.map(3.56995, 0.01, 1000, 400, 0.005)
ts_y <- as.ts(lm)
dataframe_logistic <- data.frame(ts_y)
colnames(dataframe_logistic) <- c("logistic_linear")
write.csv(dataframe_logistic, "logistic_linear_time_series.csv", row.names = FALSE)