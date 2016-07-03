def jaccard_similarity(data, person1, person2):
    """
    Jaccard similarity for two persons.
    :param data: movie ratings
    :param person1: name of first person
    :param person2: name of second person
    :return: similarity score
    """
    shared_items = {}
    for item in data[person1]:
        for item in data[person2]:
            shared_items[item] = 1

    intersection = len(shared_items)
    if intersection == 0:
        return 0

    union = 0
    for item in data[person1]:
        union += 1
    for item in data[person2]:
        union += 1

    ret_val = intersection / (union - intersection)
    return ret_val