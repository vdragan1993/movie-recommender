__author__ = 'Dragan Vidakovic'
import csv
from movies import write_movie_data
from users import write_users_data

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
print("Total movies {0}".format(len(movies)))
#write_movie_data(movies)
write_users_data(users)
