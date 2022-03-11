from client import request


class Champion:
    """
    Keeps track of the name and probabilities of using each shape.

    Probabilities are given between 0.0 and 1.0. (obviously?)

    Note
    ----
    Probabilities are stored after dividing by the sum of them.
    """

    def __init__(self,
                 name: str,
                 rock: float = 1,
                 paper: float = 1,
                 scissors: float = 1) -> None:
        self._name = name
        total = rock + paper + scissors
        self._rock = rock / total
        self._paper = paper / total


    @property
    def name(self) -> str:
        return self._name


    @property
    def str_tuple(self) -> tuple[str, str, str, str]:

        """
        A tuple with strings describing the champion.

        Returns
        -------
        tuple

        Example
        -------
        >>> Champion("John").str_tuple
        ('John','0.33','0.33','0.33')
        """
        return (self.name,
                f'{self._rock:.2f}',
                f'{self._paper:.2f}',
                f'{(1-self._rock-self._paper):.2f}')
    
    
    
'''
These are pretty self-explanatory functions. Just look at the function name, input type and return type
'''
def get_all() -> list[Champion]:
    str_list = request.to_server(f"from_db=get_all=").split('+')
    return [string_to_object(champ) for champ in str_list]


def get_all_names() -> list[str]:
    return champlist_to_names(get_all())
    
    
def champlist_to_names(champlist : list[Champion]) -> list[str]:
    return [champ.name for champ in champlist]
    
    
def string_to_object(csv_string : str) -> Champion:
    champ = csv_string.split(',')
    return Champion(champ[0], float(champ[1]), float(champ[2]), float(champ[3]))


def object_from_name(name : str) -> Champion:
    for champ in get_all():
        if name == champ.name:
            return champ
        

def list_of_player_selection(player_id : int) -> list[Champion]:
    string = request.to_server(f"from_db=get_frompl={player_id}")
    return [string_to_object(champ) for champ in string.split('+')][1:]


def list_of_player_champnames(player_id : int) -> list[Champion]:
    return champlist_to_names(list_of_player_selection(player_id))



"""
Functions which interact with the databases via the server, such as adding, deleting champions. Again self-explanatory.
"""
def save_to_player_selection(champ : Champion) -> None:
    as_string = ",".join(champ.str_tuple)
    
    request.to_server(f"from_db=save_champ={as_string}")


def save_name_to_roster(champ : str) -> None:
    save_to_roster(object_from_name(champ))


def save_to_roster(champ : Champion) -> None:
    as_string = ",".join(champ.str_tuple)
    
    request.to_server(f"from_db=save_toall={as_string}")


def delete_from_roster(name : str) -> None:
    obj = object_from_name(name)
    as_string = ",".join(obj.str_tuple)
    
    print(as_string)
    request.to_server(f"from_db=delete_champ={as_string}")
