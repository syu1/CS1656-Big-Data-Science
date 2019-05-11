# Repository: project2.template
Template for Project #2 -- SQL

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Spring 2019    
> Instructor: [Alexandros Labrinidis](http://labrinidis.cs.pitt.edu)  
> 
> Assignment: #2
> Released: Feb 5, 2018  
> **Due:      Feb 17, 2018**

### Description
This is the **second assignment** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Spring 2019 semester.

### Goal
The goal of this assignment is for you to gain familiarity with SQL.

---

### What to do

In this assignment you are asked to:  
* update a skeleton Python script (`moviepro.py`) in order to read input from CSV files and insert the data into the `cs1656.sqlite` database, and   
* provide SQL queries that answer 12 questions.

The provided skeleton Python script includes database initialization commands and also includes commands to run the SQL queries and store their output in separate output files, which you should not modify. What you should update are the parts of the script that are responsible for reading in the input data (and inserting it into the database) and for specifying the 12 SQL queries.

### Database Schema

The schema of the database is embedded in the `moviepro.py` Python script and should not be modified. It is as follows:
* Actors (aid, fname, lname, gender)  
* Movies (mid, title, year, rank)  
* Directors (did, fname, lname)  
* Cast (aid, mid, role)  
* Movie_Director (did, mid)  


### Reading input from CSV files

Your program should read input from the following CSV files:
* `actors.csv`, containing data for the Actors table,  
* `cast.csv`, containing data for the Cast table,  
* `directors.csv`, containing data for the Directors table,  
* `movie_dir.csv`, containing data for the Movie_Director table, and  
* `movies.csv`, containing data for the Movies table.  

All the data should be inserted into the appropriate tables into the `cs1656.sqlite` database. Sample insert statements have been provided in the `moviepro.py` script, but you are not restricted to doing the insertions in exactly the same way.

Samples of all these files are provided as part of this repository.


### Queries

You are asked to provide SQL queries that provide answers for the following questions. Note that **actors** refers to both male and female actors, unless explicitely specified otherwise. Also note that you should not rely on the data provided in the sample CSV files for any of the answers; the datasets will be replaced with bigger files. Finally, please note that you may define views, etc, as part of other queries.

* **[Q01]** List all the actors (first and last name) who acted in at least one film in the 80s (1980-1990, both ends inclusive) and in at least one film in the 21st century (>=2000). Sort alphabetically, by the actor's last and first name. 

* **[Q02]** List all the movies (title, year) that were released in the same year as the movie entitled `"Rogue One: A Star Wars Story"`, but had a better rank (Note: the higher the value in the *rank* attribute, the better the rank of the movie). Sort alphabetically, by movie title.  

* **[Q03]** List all the actors (first and last name) who played in a Star Wars movie (i.e., title like '%Star Wars%') in decreasing order of how many Star Wars movies they appeared in. If an actor plays multiple roles in the same movie, count that still as one movie. If there is a tie, use the actor's last and first name to generate a full sorted order.

* **[Q04]** Find the actor(s) (first and last name) who **only** acted in films released before 1985. Sort alphabetically, by the actor's last and first name.  

* **[Q05]** List the top 20 directors in descending order of the number of films they directed (first name, last name, number of films directed). For simplicity, feel free to ignore ties at the number 20 spot (i.e., always show up to 20 only).   

* **[Q06]** Find the top 10 movies with the largest cast (title, number of cast members) in decreasing order. Note: show all movies in case of a tie.  

* **[Q07]** Find the movie(s) whose cast has more actresses than actors (i.e., gender=female vs gender=male).  Show the title, the number of actresses, and the number of actors in the results. Sort alphabetically, by movie title.   

* **[Q08]** Find all the actors who have worked with at least 7 different directors. Do not consider cases of self-directing (i.e., when the director is also an actor in a movie), but count all directors in a movie towards the threshold of 7 directors. Show the actor's first, last name, and the number of directors he/she has worked with. Sort in decreasing order of number of directors.

* **[Q09]** For all actors whose first name starts with an S, count the movies that he/she appeared in his/her debut year (i.e., year of their first movie). Show the actor's first and last name, plus the count. Sort by decreasing order of the count.  

* **[Q10]** Find instances of nepotism between actors and directors, i.e., an actor in a movie and the director having the same last name, but a different first name. Show the last name and the title of the movie, sorted alphabetically by last name.  

* **[Q11]** The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the *"co-acting"* graph. That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1; all actors who acted in the same film as some actor with Bacon number 1 have Bacon number 2, etc. List all actors whose Bacon number is 2 (first name, last name). You can familiarize yourself with the concept, by visiting [The Oracle of Bacon](https://oracleofbacon.org).  

* **[Q12]** Assume that the *popularity* of an actor is reflected by the average *rank* of all the movies he/she has acted in. Find the top 20 most popular actors (in descreasing order of popularity) -- list the actor's first/last name, the total number of movies he/she has acted, and his/her popularity score. For simplicity, feel free to ignore ties at the number 20 spot (i.e., always show up to 20 only).  

---

### Important notes about grading
It is absolutely imperative that your python program:  
* runs without any syntax or other errors (using Python3) -- we will run it using the following command:  
`python3 moviepro.py`  
* strictly adheres to the format specifications for input and output, as explained above.     

Failure in any of the above will result in **severe** point loss. 


### Allowed Python Libraries
You are allowed to use the following Python libraries (although not all are needed):
```
argparse
collections
csv
json
glob
math
os
pandas
re
requests
string
sqlite3
sys
time
xml
```
If you would like to use any other libraries, you must ask permission by Monday, February 11, 2019, using [piazza](http://piazza.cs1656.org).

---

### How to submit your assignment
For this assignment, you must use the repository that was created for you after visiting the classroom link. You need to update the  file `moviepro.py` as described above, and add other files that are needed for running your program. You need to make sure to commit your code to the repository provided. We will clone all repositories shortly after midnight:  
* the day of the deadline **Sunday, February 17, 2019**  
* 24 hours later (for submissions that are one day late / -5 points), and  
* 48 hours after the first deadline (for submissions that are two days late / -15 points). 

Our assumption is that everybody will submit on the first deadline. If you want us to grade a late submission, you need to email us at `cs1656-staff@cs.pitt.edu`


### About your github account
It is very important that:  
* Your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  
* You use the same github account for the duration of the course.  
* You use the github account that you specified during the test assignment.    
