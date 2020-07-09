CREATE TABLE team_player (id integer primary key AUTOINCREMENT, team_id integer, player_id integer);
CREATE TABLE player (id integer primary key AUTOINCREMENT, name varchar);
CREATE TABLE game (id integer primary key AUTOINCREMENT );
CREATE TABLE game_team_score (id integer primary key AUTOINCREMENT, game_id integer, team_id integer, team_score integer);
CREATE TABLE team (id integer PRIMARY KEY AUTOINCREMENT );
create view all_games (id, game_id, ta_p1, ta_p2, ta_score, tb_p1, tb_p2, tb_score) as
select t1g.id, t1g.game_id, a1.name, a2.name, t1g.team_score, b1.name, b2.name, t2g.team_score
  from player a1, player a2, player b1, player b2,
    team_player a1t, team_player a2t, team_player b1t, team_player b2t,
    game_team_score t1g, game_team_score t2g
  where
      a1t.player_id = a1.id and a2t.player_id = a2.id and a1t.team_id = a2t.team_id and a1t.player_id < a2t.player_id
    and b1t.player_id = b1.id and b2t.player_id = b2.id and b1t.team_id = b2t.team_id and b1t.player_id < b2t.player_id
    and t1g.team_id = a1t.team_id and t2g.team_id = b1t.team_id
    and t1g.team_id < t2g.team_id
    and t1g.game_id = t2g.game_id;
