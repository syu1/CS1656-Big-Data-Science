import sqlite3 as lite
import csv
import re
list_of_files= ["actors.csv","cast.csv","directors.csv","movie_dir.csv","movies.csv"]
def read_files(cur):
    for file in list_of_files:
        fp = open(file,"r")
        lines = fp.readlines
        if file =="actors.csv":
            for line in lines:
                line.split(",")
                cur.execute("INSERT INTO Actors VALUES(line)")
        elif file == "cast.csv":
            for line in lines:
                cur.execute("INSERT INTO Cast VALUES(S)")
        elif file =="directors.csv":
            for line in lines:
                cur.execute("INSERT INTO directors VALUES(S)")
        elif file == "movie_dir.csv":
            for line in lines:
                cur.execute("INSERT INTO Movie_Director VALUES(S)")
        elif file == "movies.csv":
            for line in lines:
                cur.execute("INSERT INTO Movies VALUES(S)")
con = lite.connect('cs1656.sqlite')
with con:
	cur = con.cursor() 

	########################################################################		
	### CREATE TABLES ######################################################
	########################################################################		
	# DO NOT MODIFY - START 
	cur.execute('DROP TABLE IF EXISTS Actors')
	cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

	cur.execute('DROP TABLE IF EXISTS Movies')
	cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

	cur.execute('DROP TABLE IF EXISTS Directors')
	cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

	cur.execute('DROP TABLE IF EXISTS Cast1')
	cur.execute("CREATE TABLE Cast1(aid INT, mid INT, role TEXT)")

	cur.execute('DROP TABLE IF EXISTS Movie_Director')
	cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
	# DO NOT MODIFY - END

	########################################################################		
	### READ DATA FROM FILES ###############################################
	########################################################################		
	# actors.csv, Cast1.csv, directors.csv, movie_dir.csv, movies.csv
	# UPDATE THIS







	########################################################################		
	### INSERT DATA INTO DATABASE ##########################################
	########################################################################		
	# UPDATE THIS TO WORK WITH DATA READ IN FROM CSV FILES
	cur.execute("INSERT INTO Actors VALUES(1001, 'Harrison', 'Ford', 'Male')") 
	cur.execute("INSERT INTO Actors VALUES(1002, 'Daisy', 'Ridley', 'Female')")   

	cur.execute("INSERT INTO Movies VALUES(101, 'Star Wars VII: The Force Awakens', 2015, 8.2)") 
	cur.execute("INSERT INTO Movies VALUES(102, 'Rogue One: A Star Wars Story', 2016, 8.0)")
	
	cur.execute("INSERT INTO Cast1 VALUES(1001, 101, 'Han Solo')")  
	cur.execute("INSERT INTO Cast1 VALUES(1002, 101, 'Rey')")  

	cur.execute("INSERT INTO Directors VALUES(5000, 'J.J.', 'Abrams')")  
	
	cur.execute("INSERT INTO Movie_Director VALUES(5000, 101)")  

	con.commit()
    
    	

	########################################################################		
	### QUERY SECTION ######################################################
	########################################################################		
	queries = {}

	# DO NOT MODIFY - START 	
	# DEBUG: all_movies ########################
	queries['all_movies'] = '''
SELECT * FROM Movies
'''	
	# DEBUG: all_actors ########################
	queries['all_actors'] = '''
SELECT * FROM Actors
'''	
	# DEBUG: all_Cast1 ########################
	queries['all_Cast1'] = '''
SELECT * FROM Cast1
'''	
	# DEBUG: all_directors ########################
	queries['all_directors'] = '''
SELECT * FROM Directors
'''	
	# DEBUG: all_movie_dir ########################
	queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''	
	# DO NOT MODIFY - END

	########################################################################		
	### INSERT YOUR QUERIES HERE ###########################################
	########################################################################		
	# NOTE: You are allowed to also include other queries here (e.g., 
	# for creating views), that will be executed in alphabetical order.
	# We will grade your program based on the output files q01.csv, 
	# q02.csv, ..., q12.csv

	# Q01 ########################		
	queries['q01'] = '''
	SELECT Movies.title, Actors.fname, Actors.lname FROM Actors
	LEFT JOIN Cast1 ON Cast1.aid = Actors.aid
	LEFT JOIN Movies ON Movies.mid = Cast1.mid
	WHERE Movies.year >= 1980 AND Movies.year <=1980 AND EXISTS
	(
		SELECT *
		FROM Movies
		WHERE Cast1.aid = Actors.aid AND Movies.mid = Cast1.mid AND Movies.year >= 2000
	)
	ORDER BY Actors.lname ASC, Actors.fname ASC
'''	
	
	# Q02 ########################		
	queries['q02'] = '''
    SELECT Movies.title, Movies.year FROM Movies
    WHERE Movies.title = "Rouge One: A Star Wars Story" AND Movies.year =
    (Select Movies.year FROM Movies
    WHERE Movies.title = "Rouge One: A Star Wars Story"
    )
    AND Movies.rank > (Select Movies.rank FROM Movies
    WHERE Movies.title = "Rouge One: A Star Wars Story")
    ORDER BY Movies.title ASC;
'''	

	# Q03 ########################		
	queries['q03'] = '''
    SELECT Actors.fname, Actors.lname, COUNT(Movies.title) FROM Actors,Movies
    WHERE Movies.title = "%Star Wars%"
    GROUP BY Actors.fname, Actors.lname
    ORDER BY Actors.lname ASC, Actors.fname ASC;
'''	

	# Q04 ########################		
	queries['q04'] = '''
    SELECT Actors.fname,Actors.lname FROM Actors
    LEFT JOIN Cast1 ON Cast1.aid = Actors.aid
	LEFT JOIN Movies ON Movies.mid = Cast1.mid
    WHERE Movies.year < 1985
    ORDER BY Actors.lname ASC, Actors.fname ASC;
'''	

	# Q05 ########################		
	queries['q05'] = '''
    SELECT Directors.fname, Directors.lname, COUNT(Movies.title) FROM Directors
    LEFT JOIN Movie_Director ON Movie_Director.did = Directors.did
    LEFT JOIN Movies ON Movies.mid = Movie_Director.mid
    GROUP BY Directors.fname,Directors.lname
    ORDER BY COUNT(Movies.title)
    LIMIT 20;
'''	

	# Q06 ########################		
	queries['q06'] = '''
    SELECT Movies.title,COUNT(Cast1.role) FROM Movies
    LEFT JOIN Cast1 ON Cast1.mid = Movies.mid
    GROUP BY Movies.title
    ORDER BY COUNT(Cast1.role) DESC
'''	

	# Q07 ########################		
	queries['q07'] = '''
    SELECT Movies.title COUNT(Actors.gender) as FEMALES FROM Movies
    LEFT JOIN Cast1 ON Cast1.mid = Movies.mid
    LEFT JOIN Cast1 ON Cast1.aid = Actors.aid
    WHERE Actors.gender = "Female"
    
    SELECT Movies.title COUNT(Actors.gender) as FEMALES FROM Movies
    LEFT JOIN Cast1 ON Cast1.mid = Movies.mid
    LEFT JOIN Cast1 ON Cast1.aid = Actors.aid
    WHERE Actors.gender = "Male"
'''	

	# Q08 ########################		
	queries['q08'] = '''
'''	

	# Q09 ########################		
	queries['q09'] = '''
'''	

	# Q10 ########################		
	queries['q10'] = '''
'''	

	# Q11 ########################		
	queries['q11'] = '''
'''	

	# Q12 ########################		
	queries['q12'] = '''
'''	


	########################################################################		
	### SAVE RESULTS TO FILES ##############################################
	########################################################################		
	# DO NOT MODIFY - START 	
	for (qkey, qstring) in sorted(queries.items()):
		try:
			cur.execute(qstring)
			all_rows = cur.fetchall()
			
			print ("=========== ",qkey," QUERY ======================")
			print (qstring)
			print ("----------- ",qkey," RESULTS --------------------")
			for row in all_rows:
				print (row)
			print (" ")

			save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
			if (save_to_file):
				with open(qkey+'.csv', 'w') as f:
					writer = csv.writer(f)
					writer.writerows(all_rows)
					f.close()
				print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")
		
		except lite.Error as e:
			print ("An error occurred:", e.args[0])
	# DO NOT MODIFY - END
	
