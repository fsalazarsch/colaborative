print("STARTING HitscoreModel.R")
require(rjson)
require(RPostgreSQL)


args <- commandArgs(trailingOnly = FALSE)
path <- args[4]
path <- gsub("--file=", "", path)
path <- gsub("compute_hitscore.R", "", path)
hitscoremodel_id <- as.numeric(as.character(args[6]))
point_id <- as.numeric(as.character(args[7]))

dbname <- 'hitmap'
dbuser <- 'hitmap'
dbpassword <- 'hitmap'
dbhost <- 'localhost'
dbport <- 5432


drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname=dbname, user=dbuser, password=dbpassword, host=dbhost, port=dbport)


query <- "INSERT INTO project_hitscorevalue (hitscoremodel_id, point_id, value, datetime) VALUES ("
query <- paste0(query, hitscoremodel_id, ", ")
query <- paste0(query, point_id, ", ")
query <- paste0(query, rnorm(1,100,20), ", '")
query <- paste0(query, strftime(Sys.time()), "');")
dbGetQuery(con, query)

postgresqlCloseConnection(con)
postgresqlCloseDriver(drv)


