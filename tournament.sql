-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE DATABASE tournament;

\c tournament

CREATE TABLE players
(
    plyid serial primary key,
    ply_name text
);

CREATE TABLE matches
(
    mtcid serial primary key,
    winner int REFERENCES players (plyid), 
    loser int REFERENCES players (plyid)
);
