setwd("/Users/ethan/702_final_project/r")

# Read in games
games <- read.csv("../data/combined_games.csv", header = T, sep=",", row.names = NULL)
View(games)