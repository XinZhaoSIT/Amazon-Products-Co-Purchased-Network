library(sna)
library(ergm)
library(tidyverse)
library(igraph)
library(multiplex)
library(tidyverse)
library(ggplot2)

amazon_net <- read_csv(file="edge_list_select.csv")
amazon_netm <- as.matrix(amazon_net[,1:2])
amazon_g <- graph_from_edgelist(amazon_netm, directed = F)
is.weighted(amazon_g)

amazonattr <- read_csv(file="attr.csv")
amazons <- merge(amazon_net,amazonattr,by.x = "source", by.y = "Id",sort = F)
head(amazons)

V(amazon_g)$title <- amazons$label
V(amazon_g)$group <- amazons$group
V(amazon_g)$sales <- amazons$sales_rank
V(amazon_g)$category <- amazons$category
V(amazon_g)$avg_rating <- amazons$avg_rating

vcount(amazon_g)
ecount(amazon_g)
graph.density(amazon_g)
degree(amazon_g)
transitivity(amazon_g, type = "undirected")
centralization.degree(amazon_g)
centralization.degree(amazon_g)$centralization

centralization.closeness(amazon_g)$centralization
centralization.betweenness(amazon_g)$centralization
centralization.evcent(amazon_g)$centralization




