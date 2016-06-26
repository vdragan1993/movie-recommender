__author__ = 'Dragan Vidakovic'
import json
import omdb


def write_movie_data(movies):
    """
    Write data about movies to single json file
    :param movies: list of movie titles
    :return: json file of movies data
    """
    all_movies = []
    lines = []
    for movie in movies:
        search = omdb.search(movie)
        if len(search) > 0:
            hit = search[0]
            # collect data for every movie
            if hit.type == 'movie':
                # list of all movies with links
                imdb_id = hit.imdb_id
                link = get_imdb_link(imdb_id)
                poster = hit.poster
                year = hit.year
                # list of all movies
                line = movie + "," + link + "\n"
                lines.append(line)
                # extract other movies data
                movie_data = {}
                movie_data['title'] = movie
                movie_data['id'] = link
                movie_data['poster'] = poster
                movie_data['imdb_id'] = imdb_id
                movie_data['year'] = year
                omdb_data = omdb.imdbid(imdb_id)
                movie_data['imdb_rating'] = get_attribute_value(omdb_data, 'imdb_rating')
                movie_data['genre'] = get_attribute_value(omdb_data, 'genre')
                movie_data['country'] = get_attribute_value(omdb_data, 'country')
                movie_data['released'] = get_attribute_value(omdb_data, 'released')
                movie_data['runtime'] = get_attribute_value(omdb_data, 'runtime')
                movie_data['language'] = get_attribute_value(omdb_data, 'language')
                movie_data['actors'] = get_attribute_value(omdb_data, 'actors')
                movie_data['plot'] = get_attribute_value(omdb_data, 'plot')
                all_movies.append(movie_data)
                print("Completed: " + movie)
            else:
                print("Skipped: " + movie)
        else:
            print("No results: " + movie)



    # write movies
    with open('movies.json', 'w') as fp:
        json.dump(all_movies, fp, indent=4)

    # write movies with links
    f = open('links.txt', 'w')
    f.writelines(lines)
    f.close()


def get_imdb_link(imdb_id):
    """
    Creates complete imdb link for given imdb id of movie
    :param imdb_id: imdb id of movie
    :return: imdb link
    """
    return "http://www.imdb.com/title/" + imdb_id + "/"


def get_attribute_value(omdb_data, attribute):
    """
    Returns value for given attribute
    :param omdb_data: data fetched from omdb
    :param attribute: selected attribute
    :return: attribte value or empty string
    """
    ret_val = ""
    try:
        ret_val = omdb_data[attribute]
    except:
        pass
    return ret_val