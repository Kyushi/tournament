#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM matches")
    conn.commit()
    conn.close()
    return


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM players")
    conn.commit()
    conn.close()
    return


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM players")
    rows = cur.fetchone()
    conn.close()
    count = rows[0] if rows else 0
    return count



def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    # use query parameter to pass player name to query
    cur.execute("INSERT INTO players (name) VALUES(%s)", (name,))
    conn.commit()
    conn.close()
    return

def get_players():
    """Returns a list of all registered players.

     Returns:
     A list of tuples with all players (id, name) that are registered for the
     tournament.
    """
    query = """SELECT * FROM players"""
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    # create list of tuples of players with id and name from results
    players = [(row[0], row[1]) for row in rows]
    return players

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # Select player ID, name from payers table, and count wins and total matches
    # from matches for each player, order by wins and totals. Creation of view
    # is not necessary here because this does not need to be used elsewhere.
    query = """
            SELECT players.pid, players.name,
                (SELECT count(winner)
                 FROM matches
                 WHERE players.pid = winner) as wins,
                (SELECT count(*)
                 FROM matches
                 WHERE players.pid = winner OR players.pid = loser) as total
            FROM players
            ORDER BY wins DESC, total DESC
            """
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = """INSERT INTO matches (winner, loser) VALUES(%s,%s)"""
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, (winner, loser))
    conn.commit()
    conn.close()
    return


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairings = []
    # iterate through latest standings. Pairs players 1&2, 3&4 etc.
    i = 0
    while i < len(standings):
        pairings.append((standings[i][0], \
                        standings[i][1], \
                        standings[i+1][0], \
                        standings[i+1][1]))
        i += 2
    return pairings
