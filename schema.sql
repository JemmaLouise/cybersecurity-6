CREATE DATABASE movies;
USE movies;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP
);