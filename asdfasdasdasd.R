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

# set parameters for RPA plots (same for all days)
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
plot(x,y)
ts_y <- as.ts(y)
rpa_y = crqa(ts_y, ts_y, delay, embed, rescale, radius, normalize, mindiagline,minvertline, tw, whiteline, recpt, side, checkl)

# create tec plot as image in working dir
png("sin.png",width=3.25,height=3.25,units="in",res=1000,pointsize=3)
RP = rpa_y$RP
plotRP(RP, par)
dev.off()