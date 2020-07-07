CREATE TABLE team_player (team_id integer, player_id integer);
CREATE TABLE player (id integer primary key AUTOINCREMENT, name varchar);
CREATE TABLE game (id integer primary key AUTOINCREMENT );
CREATE TABLE game_team_score (game_id integer, team_id integer, team_score integer);
CREATE TABLE team (id integer PRIMARY KEY AUTOINCREMENT );
