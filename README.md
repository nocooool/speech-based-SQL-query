# speech-based-SQL-query

Hello reader. This is one of my first commits.
This repository is for one of my personal projects related to DBMS -Speech based SQL query system.

It is based on MySQL - Python connectivity

Using speechRecognition and text to speech libraries in Python, the speech input is recognized by Google API and the transcribed text
is used to form a syntactically and logically correct SQL query using functions defined in source code to perform the following:-

- Show list of Databases
- Select a Database from the list
- Show list of Tables in that database 
- Show Table Data with the following functionalities:
  - select a particular set of columns for display
  - use of aggregate functions
  - use of a where condition 
  - use of group by clause
  - use of order by clause
- Update Table with provided set and where conditions
- Delete Table tuples satisfying the provided where condition
- Write Query 
- Speak Query (Only Suitable for easy to speak queries to ensure corresct formation of query)

I have tried to provide necessary comments in source code for better understanding.  :)

Due to complexity of SQL queries, because of nesting and specific column names, 
and inability of speech to be recognized and transcribed perfectly some concepts like
creation, insertion, joins, triggers, sequences, index, etc. are not yet covered via 
speech to text mechanism but user may implement them via write query.

Suggestions are always welcome.