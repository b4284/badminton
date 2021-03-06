#!/bin/bash

set -euo pipefail

echo -ne "Content-type: text/html\n\n"

cat header.html

if [[ -z "$QUERY_STRING" ]]; then
    echo '<meta http-equiv="refresh" content="1; url=/badminton/"><p>No game selected for deletion...</p>'
else
    readarray -d \& -t VARS <<< $(echo $QUERY_STRING)
    for VAR in "${VARS[@]}"; do
        read "${VAR%=*}" <<< "${VAR#*=}"
    done

    if [[ "${DELETE:-NO}" != "YES" ]]; then
        cat <<EOF
<form>
<p>
Are you sure you want to delete the game? ($(sqlite3 ${BADMINTON_ENV:-prod}.db "$(printf 'select * from all_games where game_id = %s' $GAME_ID)"))</p>
<p><input type="hidden" name="GAME_ID" value="$GAME_ID" /></p>
<p><input type="submit" name="DELETE" value="YES" /></p>
</form>
EOF

    else
        sqlite3 ${BADMINTON_ENV:-prod}.db "$(cat <<EOF
begin transaction;
delete from team_player where team_id in (select team_id from game_team_score where game_id = $GAME_ID);
delete from game_team_score where game_id = $GAME_ID;
commit;
EOF
)"
        if [[ $? -eq 0 ]]; then
            echo '<meta http-equiv="refresh" content="1; url=/badminton/"><p>DELETED...</p>'
        else
            echo "<p>NONO</p>"
        fi
    fi
fi

cat footer.html
