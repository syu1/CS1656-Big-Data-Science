import getpass
from neo4j.v1 import GraphDatabase, basic_auth
neopass = "123" # replace this with the password you set for your database
uri = "bolt://localhost:7687" # replace this with the bolt address
#connection with authentication
driver = GraphDatabase.driver( uri, auth=basic_auth("neo4j", neopass) )
# connection without authentication

session = driver.session()
transaction = session.begin_transaction()
output_string = "### Q1 ###\n"

#[Q1] List the first 20 actors in descending order of the number of films they acted in.
query_result = transaction.run(
    "MATCH (a:Actor) -[:ACTS_IN]-> (m:Movie) RETURN a.name, COUNT(m.title) AS count ORDER BY COUNT(m.title) DESC LIMIT 20"
)
for row in query_result:
    output_string += str(row['a.name']) + ', ' + str(row['count']) + '\n'


#[Q2] List the titles of all movies with a review with at most 3 stars.
query_result = transaction.run(
    "MATCH (u:User) -[r:RATED]-> (m:Movie) WHERE r.stars <= 3 RETURN m.title"
)

output_string += '\n### Q2 ###\n'
for row in query_result:
    output_string += str(row['m.title']) + '\n'


#[Q3] Find the movie with the largest cast, out of the list of movies that have a review.
query_result = transaction.run(
    "MATCH (u:User) -[:RATED]-> (m:Movie) <-[:ACTS_IN]- (a:Actor) WITH m, COUNT(distinct a) as num_cast ORDER BY num_cast DESC LIMIT 1 RETURN m.title, num_cast"
)

output_string += '\n### Q3 ###\n'
for row in query_result:
    output_string += str(row['m.title']) + ', ' + str(row['num_cast']) + '\n'


#[Q4] Find all the actors who have worked with at least 3 different directors (regardless of how many movies they acted in).
query_result = transaction.run(
    "MATCH (a:Actor)-[:ACTS_IN]-> (m:Movie) <-[:DIRECTED]-(d:Director) WITH a, count(distinct d.name) as dirs WHERE dirs >= 3 RETURN a.name, dirs"
)

output_string += '\n### Q4 ###\n'
for row in query_result:
    output_string += str(row['a.name']) + ', ' + str(row['dirs']) + '\n'


#[Q5] List all actors whose Bacon number is exactly 2 (first name, last name).
query_result = transaction.run(
    "MATCH (kb:Actor {name: 'Kevin Bacon'}) -[:ACTS_IN]-> (m:Movie) <- [:ACTS_IN]- (a: Actor) -[:ACTS_IN]-> (n:Movie) <- [:ACTS_IN]- (b:Actor) RETURN b.name"
)

output_string += '\n### Q5 ###\n'
for row in query_result:
    output_string += str(row['b.name']) + '\n'


#[Q6] List which genres have movies where Tom Hanks starred in.
query_result = transaction.run(
    "MATCH (n:Actor {name: 'Tom Hanks'}) -[:ACTS_IN]-> (m:Movie) RETURN distinct m.genre"
)

output_string += '\n### Q6 ###\n'
for row in query_result:
    output_string += str(row['m.genre']) + '\n'


#[Q7] Show which directors have directed movies in at least 2 different genres.
query_result = transaction.run(
    "MATCH (d:Director) -[:DIRECTED]-> (m:Movie) WITH d, COUNT(distinct m.genre) as num_genre WHERE num_genre >= 2 RETURN d.name, num_genre"
)

output_string += '\n### Q7 ###\n'
for row in query_result:
    output_string += str(row['d.name']) + ', ' + str(row['num_genre']) + '\n'


#[Q8] Show the top 5 pairs of actor, director combinations, in descending order of frequency of occurrence.
query_result = transaction.run(
    "MATCH (a:Actor) -[:ACTS_IN]-> (m:Movie) <-[:DIRECTED]- (d:Director) WITH a, d, COUNT((m)) as num ORDER BY num DESC LIMIT 5 RETURN d.name, a.name, num"
)

output_string += '\n### Q8 ###\n'
for row in query_result:
    output_string += str(row['d.name']) + ', ' + str(row['a.name']) + '\n'


with open("output.txt", "w", encoding = "utf-8") as output_txt:
    output_txt.write(output_string)

transaction.close()
session.close()
