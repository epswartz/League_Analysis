set.seed(15)
library(lattice) # for xyplot
library(lme4)
library(dplyr)
library(pROC)
library(arm) # for binnedplot
library(rms) # for VIF
#library(leaps) #stepwise selection

# if you run this, obviously the following line needs to change
setwd("/Users/ethan/702_final_project/r")

# Read in games
games_orig = read.csv("../data/combined_games.csv",
    header = T,
    sep=",",
    row.names = NULL)
games = games_orig

# Create separate DF per class, useful for EDA
games_assassin = games[games$championClass == "Assassin",]
games_fighter = games[games$championClass == "Fighter",]
games_mage = games[games$championClass == "Mage",]
games_marksman = games[games$championClass == "Marksman",]
games_support = games[games$championClass == "Support",]
games_tank = games[games$championClass == "Tank",]

# EDA

table(games$firstBloodKill, games$win)

par(mfrow=c(2,2))
boxplot(goldEarned ~ win,
    data = games,
    col=rainbow(10))
boxplot(fiveMinuteGoldDelta ~ win,
    data = games,
    col=rainbow(10))
boxplot(fiveMinuteXPDelta ~ win,
    data = games,
    col=rainbow(10))
boxplot(goldEarned ~ championClass,
    data = games,
    col=rainbow(10))

binnedplot(y=games$win,games$fiveMinuteGoldDelta,
    xlab="5MGD",
    ylim=c(0,1),
    col.pts="navy",
    ylab ="Win?",
    main="Binned 5MGD vs. Win",
    col.int="white")


# binnedplots by class w/ 5MGD
par(mfrow=c(2,3))

binnedplot(y=games_assassin$win,games_assassin$fiveMinuteGoldDelta,xlab="5MGD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Assassin",
           col.int="white")
binnedplot(y=games_fighter$win,games_fighter$fiveMinuteGoldDelta,xlab="5MGD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Fighter",
           col.int="white")
binnedplot(y=games_mage$win,games_mage$fiveMinuteGoldDelta,xlab="5MGD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Mage",
           col.int="white")
binnedplot(y=games_marksman$win,games_marksman$fiveMinuteGoldDelta,xlab="5MGD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Marksman",
           col.int="white")
binnedplot(y=games_support$win,games_support$fiveMinuteGoldDelta,xlab="5MGD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Support",
           col.int="white")
binnedplot(y=games_tank$win,games_tank$fiveMinuteGoldDelta,xlab="5MGD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Tank",
           col.int="white")

par(mfrow=c(2,3))

binnedplot(y=games_assassin$win,games_assassin$fiveMinuteXPDelta,xlab="5MXPD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Assassin",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_fighter$win,games_fighter$fiveMinuteXPDelta,xlab="5MXPD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Fighter",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_mage$win,games_mage$fiveMinuteXPDelta,xlab="5MXPD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Mage",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_marksman$win,games_marksman$fiveMinuteXPDelta,xlab="5MXPD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Marksman",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_support$win,games_support$fiveMinuteXPDelta,xlab="5MXPD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Support",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_tank$win,games_tank$fiveMinuteXPDelta,xlab="5MXPD",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Tank",
           col.int="white") # this is to set the SD lines to white and ignore them


par(mfrow=c(2,3))

binnedplot(y=games_assassin$win,games_assassin$kills,xlab="Kills",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Assassin",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_fighter$win,games_fighter$kills,xlab="Kills",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Fighter",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_mage$win,games_mage$kills,xlab="Kills",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Mage",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_marksman$win,games_marksman$kills,xlab="Kills",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Marksman",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_support$win,games_support$kills,xlab="Kills",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Support",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_tank$win,games_tank$kills,xlab="Kills",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Tank",
           col.int="white") # this is to set the SD lines to white and ignore them

par(mfrow=c(2,3))

binnedplot(y=games_assassin$win,games_assassin$visionScore,xlab="Vision Score",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Assassin",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_fighter$win,games_fighter$visionScore,xlab="Vision Score",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Fighter",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_mage$win,games_mage$visionScore,xlab="Vision Score",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Mage",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_marksman$win,games_marksman$visionScore,xlab="Vision Score",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Marksman",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_support$win,games_support$visionScore,xlab="Vision Score",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Support",
           col.int="white") # this is to set the SD lines to white and ignore them
binnedplot(y=games_tank$win,games_tank$visionScore,xlab="Vision Score",ylim=c(0,1),col.pts="navy",
           ylab ="Win?",main="Tank",
           col.int="white") # this is to set the SD lines to white and ignore them


par(mfrow=c(1,1))

xyplot(goldEarned ~ fiveMinuteGoldDelta, data=games)
#plot()

# Model
model_simple = glm(win ~ fiveMinuteGoldDelta +
    fiveMinuteXPDelta +
    firstDragon,
    data=games,
    family=binomial(link="logit"))

model_full = glm(win ~ fiveMinuteGoldDelta +
    championClass +
    firstBloodKill +
    kills +
    deaths +
    assists +
    ccScore +
    wardKills +
    firstDragon +
    championClass*firstBloodKill +
    championClass*kills +
    championClass*deaths +
    championClass*firstDragon +
    championClass*fiveMinuteGoldDelta +
    championClass*fiveMinuteXPDelta +
    fiveMinuteXPDelta +
    firstTower,
    data=games,
    family=binomial(link="logit"))

# Backward selection
#FullModel <- glm(formula = , data = games, family=binomial(link="logit"))

n <-  nrow(games)
model_backward_bic <- step(model_full,direction="backward",trace=0,k = log(n))
model_backward_aic <- step(model_full,direction="backward",trace=0,k = 2)

roc(games$win,fitted(model_backward_aic),
    plot=T,print.thres="best",legacy.axes=T,
    print.auc =T,col="red3")

binnedplot(predict(model_backward_aic, type="response"),residuals(model_backward_aic,"resp"),xlab="Expected Value",
           col.int="red4",ylab="Avg. residuals",main="Binned residual plot",col.pts="navy")