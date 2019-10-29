setwd("~/Desktop/ECON/Micro/DeBacker/Git/CompEcon_Fall19/ProblemSets/ProblemSet5")
library(fredr)
library(purrr)
library(TSA)
library(reshape2)
library(dse)
library(rdd)
library(xtable)

fredr_set_key("4a92891d6d4b0f01c34c0466822da6f5")

# Retrieve data
params <- list(series_id = c("USREC",  "FEDFUNDS", "GDPPOT", "GDPC1", "GDPDEF"), 
               frequency = c("q", "q", "q", "q", "q")
               )
intData = purrr::pmap_dfr(
  .l = params,
  .f = ~ fredr(series_id = .x, frequency = .y, observation_start = as.Date("1960-01-01"))
)

intDataM <- melt(intData, id = c("series_id", "date"))
intRate <- dcast(intDataM, formula = date ~ series_id, value.var = "value")
# Calculate percent deviation of GDP from potential GDP
intRate$dev <- 100*(intRate$GDPC1 - intRate$GDPPOT)/ intRate$GDPPOT
# Calculate percent inflation (percent change in GDP deflator)
intRate$infl <- NA
for (i in 2:nrow(intRate)) {
  intRate$infl[i] <- 100*(intRate$GDPDEF[i] - intRate$GDPDEF[i-1])/intRate$GDPDEF[i-1]
}

# Linear model of federal funds rate as explined by deviation of GDP and inflation rate
linreg = lm(intRate$FEDFUNDS ~ intRate$dev + intRate$infl)
# Summary output of regression
summary(linreg)
print(xtable(linreg))

# intRate['tr'] = (intRate['infl'] + 2) + (0.5*(intRate['infl'] - 2)) + (0.5*intRate['dev'])
intRate$tr <- (intRate$infl + 2) + (0.5*(intRate$infl -2 )) + (0.5*intRate$dev)

linreg2 = lm(intRate$FEDFUNDS ~ intRate$tr + intRate$USREC)
print(xtable(linreg2))
