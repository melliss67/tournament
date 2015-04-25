#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    query = "select count(plyid) from players as player_count;"
    db = connect()
    c = db.cursor()
    c.execute(query)
    row = c.fetchone()
    count = int(row[0])
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (ply_name) values(%s)", (name,))
    db.commit()
    db.close()


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

    query = "select plyid, ply_name, count(win.winner) as wins, count(loss.loser) as loses from players left join matches win on win.winner = players.plyid left join matches loss on loss.loser = players.plyid group by plyid, ply_name order by count(win.winner) desc;"
    db = connect()
    c = db.cursor()
    c.execute(query)
    players = [(row[0], str(row[1]), int(row[2]), int(row[2] + row[3])) for row in c.fetchall()]
    return players

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db = connect()
    c = db.cursor()
    c.execute("insert into matches (winner, loser) values(%s,%s)", (winner,loser))
    db.commit()
    db.close()
 
 
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

    players = playerStandings()
    i = 0
    pairings = ()
    while i < len(players):
        p1 = players[i]
        i = i + 1
        p2 = players[i]
        i = i + 1
        pairings = pairings + ((p1[0],p1[1],p2[0],p2[1]),)

    return pairings
