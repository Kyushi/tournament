-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create brand new tournament database (drop previous if exists)
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
-- Connect to tournament db
\c tournament;

-- Create table players, only serial (ID) and name necessary
CREATE TABLE players (
  pid serial PRIMARY KEY,
  name text
);

-- Create table matches with serial (ID), winner, loser as id referenced from
-- players table
CREATE TABLE matches (
  mid serial PRIMARY KEY,
  winner integer references players (pid),
  loser integer references players (pid)
);
