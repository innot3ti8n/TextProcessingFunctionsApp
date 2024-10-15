from collections import namedtuple

# result item container
Result = namedtuple("Result", ['comp_id', 'start', 'end', 'flag'])

def filterListBy(my_list, condition):
    return list(filter(condition, my_list))