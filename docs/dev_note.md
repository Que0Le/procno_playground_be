Lots of problem with parsing result from raw sql statements.
See 
https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.from_statement
https://docs.sqlalchemy.org/en/14/orm/tutorial.html#using-textual-sql



## How upload record works
- Send Post request to /records: 
Server create a random filename length 32, check if record dir has file with name like that, write to DB, and return filename to client.

- Upload file using filename. 
