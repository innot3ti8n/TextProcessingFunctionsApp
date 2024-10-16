from dataclasses import dataclass

# result item container
@dataclass
class Result:
    comp_id: int
    start: int
    end: int
    flag: int = None

def filterListBy(my_list, condition):
    return list(filter(condition, my_list))