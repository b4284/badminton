#!/bin/bash

set -euo pipefail

echo -ne "Content-type: text/html\n\n"

readarray -t GAMES <<< $(sqlite3 badminton.db "select id, game_id, ta_p1, ta_p2, ta_score, tb_p1, tb_p2, tb_score from all_games;")

function generate_games_table {
    for GAME in "${GAMES[@]}"; do
        readarray -d \| -t GAME_DETAIL <<< "$(echo "$GAME")" 
        echo "<tr>"
        echo "<td><input type=\"radio\" name=\"DELETE_ID\" value=\"${GAME_DETAIL[0]}\" /></td>"
        for i in $(seq 1 7); do
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
    <tr><th></th><th>GAME #</th><th>P1</th><th>P2</th><th>TEAM A</th><th>P1</th><th>P2</th><th>TEAM B</th></tr>
    $(generate_games_table)
    </table>
  </body>
</html>
EOF
