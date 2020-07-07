#!/bin/bash

set -euo pipefail

if [[ "x${QUERY_STRING}" != "x" ]]; then
    function new_game {
        local TAP1="$1"
        local TAP2="$2"
        local TBP1="$3"
        local TBP2="$4"
        local TA_SCORE="$5"
        local TB_SCORE="$6"

        sqlite3 badminton.db "$(cat <<EOF
begin transaction;
insert into game default values;

insert into team default values;
insert into game_team_score values ((select max(id) from game), (select max(id) from team), $TA_SCORE);
insert into team_player values ((select max(id) from team), $TAP1);
$(if [[ "x$TAP2" != "x" ]]; then echo "insert into team_player values ((select max(id) from team), $TAP2);"; fi)

insert into team default values;
insert into game_team_score values ((select max(id) from game), (select max(id) from team), $TB_SCORE);
insert into team_player values ((select max(id) from team), $TBP1);
$(if [[ "x$TBP2" != "x" ]]; then echo "insert into team_player values ((select max(id) from team), $TBP2);"; fi)

commit;
EOF
)"
    }
    
    echo -ne "Content-type: text/html\n\n"

    readarray -d \& -t VARS <<< $(echo $QUERY_STRING)
    for VAR in "${VARS[@]}"; do
        read "${VAR%=*}" <<< "${VAR#*=}"
    done
    
    if [[ "x$TAP1" != "x" && "x$TBP1" != "x" &&
              "x$TA_SCORE" != "x" && "x$TB_SCORE" != "x" &&
              "x$(echo "$TA_SCORE" |sed 's/[^0-9]//g')" == "x$TA_SCORE" &&
              "x$(echo "$TB_SCORE" |sed 's/[^0-9]//g')" == "x$TB_SCORE"
        ]]
    then
        if new_game "$TAP1" "$TAP2" "$TBP1" "$TBP2" "$TA_SCORE" "$TB_SCORE"; then
            cat <<EOF
<!doctype html>
<html>
  <head>
    <meta http-equiv="refresh" content="1; url=/badminton/">
  </head>
  <body>
    <h1>OK...</h1>
  </body>
</html>
EOF
        else
            echo NONO2            
        fi
    else
        echo NONONO
    fi
else
    function generate_select_box {
        local NAME="$1"
        local NULLABLE="$2"
        echo "<select name=\"$NAME\">"
        if [[ "x${NULLABLE}" == "x1" ]]; then
            echo "<option value=\"\"></option>"
        fi
        for ROW in "${PLAYERS[@]}"; do
            I=${ROW%|*}
            NAME=${ROW#*|}
            echo "<option value=\"$I\">$NAME</option>"
        done
        echo "</select>"
    }

    echo -ne "Content-type: text/html\n\n"

    readarray -t PLAYERS <<< $(sqlite3 badminton.db 'select * from player;')

    cat <<EOF
<!doctype html>
<html>
  <body>
    <form>
      <h1>TEAM A</h1>
      <div>SCORE: <input type="number" name="TA_SCORE" /></div>
      <div>PLAYER 1: $(generate_select_box TAP1 0)</div>
      <div>PLAYER 2: $(generate_select_box TAP2 1) (optional)</div>

      <h1>TEAM B</h1>
      <div>SCORE: <input type="number" name="TB_SCORE" /></div>
      <div>PLAYER 1: $(generate_select_box TBP1 0)</div>
      <div>PLAYER 2: $(generate_select_box TBP2 1) (optional)</div>

      <p><input type="submit" value="Submit" /> <a href="index.cgi"><input type="button" value="Cancel" /></a></p>
    </form>
  </body>
</html>
EOF
fi
