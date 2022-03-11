from client import request


class Player:
    '''
    Keeps track of names, colors and current points
    '''
    def __init__(self,
        name: str,
        color: str,
        id : int,
        score: int) -> None:
        
        self.name = name
        self.color = color
        self.score = score
        self.id = id


player1 = Player("Player 1", "blue", 1, 0)
player2 = Player("Player 2", "red", 2, 0)


'''
Players with current profiles
'''
def get_players() -> tuple[Player]:
    update_player_styles()
    return player1, player2


"""
Default player objects which will be altered for customization purposes later on. Prevents missing values :) :) :)
"""
def get_default_players() -> tuple[Player]:  
    return Player("Player 1", "blue", 1, 0), Player("Player 2", "red", 2, 0)


"""
Will affect the player profile of the client making the request
"""
def set_player_style(new_name : str, new_color : str) -> None: 
    request.to_server(f"set_style={new_name},{new_color}")



"""
Helper function -> update_player_styles
"""
def get_styles() -> str:
    return request.to_server(f"get_styles=")


"""
Gets the styles stored in the profile database so that it remembers your name and color
"""
def update_player_styles() -> None:
    global player1,player2
    styles = get_styles().split('+')
    
    player1style, player2style = styles[0].split(','), styles[1].split(',')
    
    player1 = Player(player1style[0], player1style[1], 1, 0)
    player2 = Player(player2style[0], player2style[1], 2, 0)
    