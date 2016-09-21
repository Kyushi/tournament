-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
  pid serial PRIMARY KEY,
  name text
);

CREATE TABLE matches (
  mid serial PRIMARY KEY,
  player_id_1 integer references players (pid),
  player_id_2 integer references players (pid),
  winner integer
);
