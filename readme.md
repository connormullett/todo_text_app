
# TODOS

## prerequisites
- python3 (obv)
- Postgresql (psql)
- psycopg2 (pip install psycopg2)
- git (obv)


## installing & Configuration
- clone repo in any folder
- create a file called settings.txt in the same directory
- add the password to this document on one line
- chmod +x 600 settings.txt
- That will make sure no other users can open your password file
- change the user in the connection string to match your postgres user
- run psql and create a database called `todos`
- run the following sql script `CREATE TABLE todo (id bigserial primary key, title varchar(20) not null, content varchar(30) not null, complete boolean not null default false, due bigint not null)`
- And that should be it, set this on a raspberry pi or stick it in your init.d folder and as long as you have your computer, you have your todos

