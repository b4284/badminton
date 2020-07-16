#!/bin/bash

set -euo pipefail

echo -ne "Content-type: text/html\n\n"

cat header.html

if [[ -z "$QUERY_STRING" ]]; then
    echo '<meta http-equiv="refresh" content="1; url=/badminton/"><p>No player selected for deletion...</p>'
else
    readarray -d \& -t VARS <<< $(echo $QUERY_STRING)
    for VAR in "${VARS[@]}"; do
        read "${VAR%=*}" <<< "${VAR#*=}"
    done

    if [[ $(sqlite3 badminton.db "select count(1) from team_player where player_id = $PLAYER_ID") -gt 0 ]]; then
       echo '<meta http-equiv="refresh" content="2; url=/badminton/"><p>Players with a game record cannot be deleted...</p>'
    else

        if [[ "${DELETEPLAYER:-NO}" != "YES" ]]; then
            cat <<EOF
<form>
<p>
Are you sure you want to delete the player? ($(sqlite3 badminton.db "$(printf 'select * from player where id = %s' $PLAYER_ID)"))</p>
<p><input type="hidden" name="PLAYER_ID" value="$PLAYER_ID" /></p>
<p><input type="submit" name="DELETEPLAYER" value="YES" /></p>
</form>
EOF

        else
            sqlite3 badminton.db "$(cat <<EOF
begin transaction;
delete from player where id = $PLAYER_ID;
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
fi

cat footer.html
