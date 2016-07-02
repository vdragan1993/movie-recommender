from pymongo import MongoClient
from math import sqrt


def form_critics():
    """
    Extracts critics data from database
    :return: critics dictionary
    """
    client = MongoClient()
    db = client.recommend
    all_users = db.users.find()
    # initialize dict
    critics = {}
    for user in all_users:
        # extract user
        user_id = user['id']
        # define user dict
        critics[user_id] = {}
        # append ratings
        ratings = user['ratings']
        for rating in ratings:
            this_movie = rating['movie']
            this_rating = rating['rating']
            critics[user_id][this_movie] = int(this_rating)

    return critics


def form_user_critics(user1, user2, critics):
    """
    Extracts critics data from critics dictionary for given users
    :param user1: id of first user
    :param user2: id of second user
    :param critics: critics dictionary
    :return: critics dictionary for given users
    """
    user_critics = {}
    user_critics[user1] = critics[user1]
    user_critics[user2] = critics[user2]
    return user_critics


def similarity_distance(data, person1, person2):
    """
    Euclidean distance-based similarity for two persons.
    Implemented to give higher values for persons who are similar.
    :param data: movie ratings
    :param person1: name of first person
    :param person2: name of second person
    :return: similarity score
    """
    # list of shared items
    shared_items = {}
    for item in data[person1]:
        if item in data[person2]:
            shared_items[item] = 1

    # no ratings in common
    if len(shared_items) == 0:
        return 0

    # calculating distance
    sum_of_squares = sum([pow(data[person1][item] - data[person2][item], 2)] for item in shared_items)
    ret_val = 1 / (1 + sqrt(sum_of_squares))
    return ret_val


def pearson_correlation(data, person1, person2):
    """
    Calculates Pearson correlation coefficient for two persons.
    :param data: move ratings
    :param person1: name of first person
    :param person2: name of second person
    :return: correlation coefficient
    """
    # list of shared items
    shared_items = {}
    for item in data[person1]:
        if item in data[person2]:
            shared_items[item] = 1

    # number of elements
    n = len(shared_items)

    # no ratings in common
    if n == 0:
        return 0

    n = float(n)

    # adding up all preferences
    sum1 = sum([data[person1][item] for item in shared_items])
    sum2 = sum([data[person2][item] for item in shared_items])

    # summing up squares
    sum_sq1 = sum([pow(data[person1][item], 2) for item in shared_items])
    sum_sq2 = sum([pow(data[person2][item], 2) for item in shared_items])

    # summing products
    p_sum = sum([data[person1][item] * data[person2][item] for item in shared_items])

    # Pearson
    num = p_sum - (sum1 * sum2 / n)
    den = sqrt((sum_sq1 - pow(sum1, 2) / n) * (sum_sq2 - pow(sum2, 2) / n))

    # avoid dividing by 0
    if den == 0:
        return 0

    ret_val = num/den

    return ret_val


def get_default_recommendations(data, person, similarity=pearson_correlation):
    """
    Gets recommendations for a person using a weighted average of positive correlated users.
    :param data: movie ratings
    :param person: given person
    :param similarity: similarity heuristics
    :return: list of recommendations with predicted ratings
    """
    totals = {}
    similarity_sums = {}
    for other in data:
        # skip myself
        if other == person:
            continue

        sim = similarity(data, person, other)
        # ignore zero or negative correlations
        if sim <= 0:
            continue

        for item in data[other]:
            # score movies person hasn't seen yet
            if item not in data[person] or data[person][item] == 0:
                # similarity * score
                totals.setdefault(item, 0)
                totals[item] += data[other][item] * sim
                # sum of similarities
                similarity_sums.setdefault(item, 0)
                similarity_sums[item] += sim

        # normalised list
        rankings = [(total / similarity_sums[item], item) for item, total in totals.items()]
        rankings.sort()
        rankings.reverse()
        return rankings