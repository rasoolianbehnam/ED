--------------------------------------------------------------------------------------------------------------------------------------------
Command                                              Action
--------------------------------------------------- -----------------------------------------------------------------------------------------
SELECT * FROM sqlol.users                             Get all fields from the table "sql.users"

SELECT * FROM sqlol.ssn                               Get all fields from the table "sql.ssn"

SELECT name FROM sqlol.ssn                            Get field "name" from the table "sql.ssn"

SELECT ssn as name FROM sqlol.ssn                     Get field "ssn" from the table "sql.ssn" and change its field name to "name"

SELECT * FROM sqlol.ssn WHERE name='Herp Derper'      Get all fields from the table "sql.ssn" with the "name" field equal to "Herp Derper"

SELECT * FROM sqlol.ssn WHERE name='Fred'             Get all fields from the table "sql.ssn" with the "name" field equal to "Fred"
SELECT * FROM sqlol.ssn WHERE name='Fred' 
OR 'a'='a'                                            Get all fields from the table "sql.ssn" (the condition is always true)

SELECT username FROM sqlol.users UNION SELECT ssn 
AS username FROM sqlol.ssn                            Combine data from two tables
--------------------------------------------------------------------------------------------------------------------------------------------


-------------------------------------------------- ----------------------------------------------------------------------------------------
SELECT * FROM sqlol.users                          Get all fields from the table "sql.users"

SELECT * FROM sqlol.ssn                            Get all fields from the table "sql.ssn"

SELECT name FROM sqlol.ssn                         Get field "name" from the table "sql.ssn"

SELECT ssn as name FROM sqlol.ssn                  Get field "ssn" from the table "sql.ssn" and change its field name to "name"

SELECT * FROM sqlol.ssn WHERE name='Herp Derper'   Get all fields from the table "sql.ssn" with the "name" field equal to "Herp Derper"

-------------------------------------------------- ----------------------------------------------------------------------------------------


