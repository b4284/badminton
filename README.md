Badminton - a score keeping web page in shell script CGI
========================================================

FILES
-----
  - badminton.sql: SQLite3 database schema file
  - index.cgi: the main page that shows all games in the database
  - newgame.cgi: a function page that adds a new game to the database

USAGE
-----
  - You must have a CGI-enabled http server to run this tool. For example,
    Apache Httpd with mod_cgi.
  - Build the SQLite3 database using the schema file.
    Something like: `sqlite3 -init badminton.sql new.db`
