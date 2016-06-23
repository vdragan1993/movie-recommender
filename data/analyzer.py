__author__ = 'Dragan Vidakovic'
import csv
import crawler
import omdb

users = []
movies = []
skip = 0
with open('training_data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        skip += 1
        if skip > 1:
            if row[0] not in users:
                users.append(row[0])
            if row[1] not in movies:
                movies.append(row[1])

print("Total users {0}".format(len(users)))
print("Total movies {0}".format(len(users)))
link, poster = crawler.get_imdb_link(movies[10])
print(link)
print(poster)
movie = omdb.imdbid('tt0080339')
print(movie)
print(movie['imdb_rating'])