#!/bin/bash

set -euo pipefail

echo -ne "Content-type: text/html\n\n"

cat header.html

readarray -t GAMES <<< $(sqlite3 ${BADMINTON_ENV:-prod}.db "select game_id, ta_p1, ta_p2, ta_score, tb_p1, tb_p2, tb_score from all_games;")
readarray -t RANKINGS <<< $(sqlite3 ${BADMINTON_ENV:-prod}.db "select id, name, score from player_score_sum;")

function generate_games_table {
    for GAME in "${GAMES[@]}"; do
        readarray -d \| -t GAME_DETAIL <<< "$(echo "$GAME")"
        echo "<tr>"
        echo "<td><input type=\"radio\" name=\"GAME_ID\" value=\"${GAME_DETAIL[0]}\" /></td>"
        for i in $(seq 0 $((${#GAME_DETAIL[@]} - 1))); do
            echo "<td>${GAME_DETAIL[$i]}</td>"
        done
        echo "</tr>"
    done
}

function generate_ranking {
    for RANK in "${RANKINGS[@]}"; do
        readarray -d \| -t RANK_DETAIL <<< "$(echo "$RANK")"
        echo "<tr>"
        echo "<td><input type=\"radio\" name=\"PLAYER_ID\" value=\"${RANK_DETAIL[0]}\" /></td>"
        for i in $(seq 0 $((${#RANK_DETAIL[@]} - 1))); do
            echo "<td>${RANK_DETAIL[$i]}</td>"
        done
        echo "</tr>"
    done
}

cat <<EOF
    <p><a href="newgame.cgi"><input type="button" value="New Game" /></a></p>
    <h1>ALL GAMES</h1>

    <form action="delete.cgi">
      <table border="1">
      <tr><th></th><th>GAME #</th><th>P1</th><th>P2</th><th>TEAM A</th><th>P1</th><th>P2</th><th>TEAM B</th></tr>
      $(generate_games_table)
      </table>
      <p><input type="submit" value="Delete game"></p>
    </form>

    <h1>RANKING</h1>
    <form>
      <table border="1">
        <tr><th></th><th>#</th><th>PLAYER</th><th>SCORE</th></tr>
        $(generate_ranking)
      </table>
      <p>
        <button type="submit" formaction="newplayer.cgi">New player</button>
        <button type="submit" formaction="deleteplayer.cgi">Delete player</button>
      </p>
    </form>
EOF

cat footer.html
