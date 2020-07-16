#!/bin/bash

set -euo pipefail

echo -ne "Content-type: text/html\n\n"

cat header.html

if [[ -n "$QUERY_STRING" ]]; then
   readarray -d \& -t VARS <<< $(echo $QUERY_STRING)
   for VAR in "${VARS[@]}"; do
       read "${VAR%=*}" <<< "${VAR#*=}"
   done
fi

if [[ "${NEWPLAYER:-NO}" != "YES" ]]; then
    cat <<EOF
<form>
<input type="hidden" name="NEWPLAYER" value="YES">
<p>Enter new player name: <input type="text" name="NAME" /></p>
<p><button type="submit">Submit</button>
</form>
EOF

else
    sqlite3 ${BADMINTON_ENV:-prod}.db "$(cat <<EOF
begin transaction;
insert into player (name) values ('$NAME');
commit;
EOF
)"
    if [[ $? -eq 0 ]]; then
        cat <<EOF
<meta http-equiv="refresh" content="1; url=/badminton/">
<p>ADDED...</p>
EOF
    else
        echo "<p>NONO</p>"
    fi
fi

cat footer.html
