-- create database and table
CREATE DATABASE moviesdataconcat;
USE moviesdataconcat;

CREATE TABLE moviedata (
  movie_id int NOT NULL,
  title VARCHAR(2000) NOT NULL,
  yrmade int DEFAULT NULL,
  isAdult VARCHAR(200) DEFAULT NULL,
  runtime int DEFAULT NULL,
  genres VARCHAR(2000) DEFAULT NULL,
  ratingavgscore int DEFAULT NULL,
  actors VARCHAR(2000) DEFAULT NULL,
  company VARCHAR(2000) DEFAULT NULL,
  agerating VARCHAR(2000) DEFAULT NULL,
  tags VARCHAR(20000) DEFAULT NULL,
  votes int DEFAULT NULL,
  PRIMARY KEY (movie_id));

-- load csv data into the tables

SET GLOBAL local_infile=1; -- loading permissions

LOAD DATA LOCAL INFILE "C:\Users\Bella\Documents\CFG Work\cfg group project\datasets\40yrskaggle\movies.csv"
INTO TABLE moviedata
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE "C:\Users\Bella\Documents\CFG Work\cfg group project\datasets\imdb\title.basics.tsv\title.basics.tsv"
INTO TABLE moviedata
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE "C:\Users\Bella\Documents\CFG Work\cfg group project\datasets\imdb\title.ratings.tsv\title.ratings.tsv"
INTO TABLE moviedata
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE "C:\Users\Bella\Documents\CFG Work\cfg group project\datasets\movielens\ml-latest-small\ml-latest-small\movies.csv"
INTO TABLE moviedata
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE "C:\Users\Bella\Documents\CFG Work\cfg group project\datasets\netflix\netflix_movies_and_tv_shows_sample_dataset_sample.csv"
INTO TABLE moviedata
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE "C:\Users\Bella\Documents\CFG Work\cfg group project\datasets\rottentomatoes\rotten_tomatoes_top_movies_2019-01-15.csv"
INTO TABLE moviedata
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

