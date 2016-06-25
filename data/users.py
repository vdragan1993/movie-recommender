__author__ = 'Dragan Vidakovic'
import json
import csv


def write_users_data(users):
    """
    Write data about users and ratings in json file
    :param users: list of users
    :return: json file of users data
    """
    # prepare all movies and dict of movies and links
    all_movies = []
    movie_links = {}
    f = open("links.txt", 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line[:-1]
        splits = line.split(',')
        movie = splits[0]
        link = splits[1]
        all_movies.append(movie)
        movie_links[movie] = link

    # prepare all users rating
    all_users = []
    for user in users:
        users = {}
        if user not in all_users:
            users['id'] = user
            users['ratings'] = []

        skip = 0
        with open('training_data.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                skip += 1
                if skip > 1:
                    if user == row[0]:
                        rate = {}
                        movie = row[1]
                        rating = int(row[2])*2
                        if movie in all_movies:
                            rate['movie'] = movie_links[movie]
                            rate['rating'] = rating
                            users['ratings'].append(rate)

        all_users.append(users)

    # write users
    with open('users.json', 'w') as fp:
        json.dump(all_users, fp, indent=4)