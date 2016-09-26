# We have a winner! #

*Project using relational database (PostgreSQL) and Python db api (psycopg2) for Udacity Full Stack Nanodegree course*

---
## Overview ##

This is a psql project for a swiss style tournament system.
This script creates two database tables: players and matches
In the player table, players can be registered with their name, which does not need to be unique. The player is given an ID (serial, auto-incrementing number).
In the 'matches' table, the results of matches between players can be entered. The matches can be evaluated and new pairs of players are automatically generated for the next round of matches.

---
## Requirements ##

* Python 2.7
* PostgreSQL

---
## Quickstart ##

1. Download or clone this repository.
2. Create `tournament` database (`create database tournament`)
3. Run tournament.sql (`psql tournament.sql`) to create players and matches tables
4. For testing, run `python tournament_test.py`
