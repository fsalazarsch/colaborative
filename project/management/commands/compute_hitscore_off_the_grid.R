print("STARTING compute_hitscore_off_the_grid.R")
require(rjson)
require(RPostgreSQL)


args <- commandArgs(trailingOnly = FALSE)

path <- args[4]
path <- gsub("--file=", "", path)
path <- gsub("compute_hitscore_off_the_grid.R", "", path)
hitscoremodel_id <- as.numeric(as.character(args[6]))
point_id <- as.numeric(as.character(args[7]))


query <- "INSERT INTO project_hitscorevalue (hitscoremodel_id, point_id, value, datetime) VALUES ("
query <- paste0(query, hitscoremodel_id, ", ")
query <- paste0(query, point_id, ", ")
query <- paste0(query, rnorm(1,100,20), ", '")
query <- paste0(query, strftime(Sys.time()), "');")


dbname <- 'hitmap'
dbuser <- 'hitmap'
dbpassword <- 'hitmap'
dbhost <- 'localhost'
dbport <- 5432

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname=dbname, user=dbuser, password=dbpassword, host=dbhost, port=dbport)

dbGetQuery(con, query)

postgresqlCloseConnection(con)
postgresqlCloseDriver(drv)
print("ENDING compute_hitscore_off_the_grid.R")


