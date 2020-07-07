#!/bin/bash

set -euo pipefail

echo -ne "Content-type: text/html\n\n"

readarray -t GAMES <<< $(sqlite3 badminton.db "$(cat <<EOF
select t1g.game_id, a1.name, a2.name, t1g.team_score, b1.name, b2.name, t2g.team_score
from player a1, player a2, player b1, player b2, 
  team_player a1t, team_player a2t, team_player b1t, team_player b2t,
  game_team_score t1g, game_team_score t2g
where 
      a1t.player_id = a1.id and a2t.player_id = a2.id and a1t.team_id = a2t.team_id and a1t.player_id < a2t.player_id
  and b1t.player_id = b1.id and b2t.player_id = b2.id and b1t.team_id = b2t.team_id and b1t.player_id < b2t.player_id
  and t1g.team_id = a1t.team_id and t2g.team_id = b1t.team_id
  and t1g.team_id < t2g.team_id
  and t1g.game_id = t2g.game_id;
EOF
)")

function generate_games_table {
    for GAME in "${GAMES[@]}"; do
        readarray -d \| -t GAME_DETAIL <<< "$(echo "$GAME")" 
        echo "<tr>" 
        for i in $(seq 0 6); do 
            echo "<td>${GAME_DETAIL[$i]}</td>"
        done 
        echo "</tr>" 
    done
}

cat <<EOF
<!doctype html>
<html>
  <body>
    <p><a href="newgame.cgi"><input type="button" value="New Game" /></a></p>
    <h1>ALL GAMES</h1>
    <table border="1">
    <tr><th>GAME #</th><th>P1</th><th>P2</th><th>TEAM A</th><th>P1</th><th>P2</th><th>TEAM B</th></tr>
    $(generate_games_table)
    </table>
  </body>
</html>
EOF
