'''
NOTE FOR T.A. WHO IS INSPECTING THIS FILE:

This is a work in progress, our current progress is:
- The game works as intended, albeit it only runs as a single-player game
- The client (pyclient.py) is connected to the server (pyserver.py) which is connected to a psuedo-database (see folder) via a reader (dbreader.py)
- The game works only if socket communication is in place, which is as instructed
- We have been able to identify the clients as seperate entitites (good), but we have not been able to use this in any meaningful way

'''

from socket import socket
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from socketio import KafkaManager
from dbreader import request

from core import Champion, Match, Shape, Team
import dbreader


def request_to_server(sock: socket, message: str) -> str:
    sock.sendall(message.encode())
    return sock.recv(4096).decode()

    
def get_current_id(sock):
    return request_to_server(sock, "check_id ")


def input_champion(sock : socket,
                   prompt: str,
                   color: str,
                   player1: list[str],
                   player2: list[str]) -> None:


    #creates an easy-access list of champion names by making a request to the database via the server
    list_of_champ_names = [champ.name for champ in list_of_champions(sock)]
    
    
    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        match Prompt.ask(f'[{color}]{prompt}'):
            case name if name not in list_of_champ_names:
                print(f'The champion {name} is not available. Try again.')
            case name if name in player1:
                print(f'{name} is already in your team. Try again.')
            case name if name in player2:
                print(f'{name} is in the enemy team. Try again.')
            case _:
                player1.append(name)
                break


def list_of_champions(sock):
    list_of_csv_strings = request_to_server(sock, f"all_champs None").split('+')
    list_of_champs = []
    
    for each in list_of_csv_strings:
        champ = each.split(',')
        list_of_champs.append(Champion(champ[0], float(champ[1]), float(champ[2]), float(champ[3])))
    
    return list_of_champs
    

def print_match_summary(match: Match) -> None:

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')

    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')
    

def print_champs(sock):

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    
    # Populate the table
    for champion in list_of_champions(sock):
        available_champs.add_row(*champion.str_tuple)

    print(available_champs)
    
    
def save_match_result(sock):
    None

    

 
if __name__ == "__main__":
    sock = socket()
    sock.connect(("localhost", 12000))
    
    player1 = []
    player2 = []
    player_id = ''
    
    
    '''
    print(check_player_connect(sock, 1))
    print(check_player_connect(sock, 2))
    
    if check_player_connect(sock, 1) == "false":
        print(request_id(sock, 1))
        player_id += request_id(sock, 1)
    elif check_player_connect(sock, 2) == "false":
        player_id += request_id(sock, 2)
    '''
    
    
    print('\n'
          'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
          '\n'
          'Each player choose a champion each time.'
          '\n\n')


    print(get_current_id(sock))
        
    print_champs(sock)
    for _ in range(2):
        input_champion(sock, "Select your champion: ", "blue", player1, player2)
        input_champion(sock, "Select your champion: ", "red", player2, player1)


    #makes champion names into champions
    for index, champ in enumerate(player1):
        for real_champ in list_of_champions(sock):
            if champ == real_champ.name:
                player1[index] = real_champ
                
    for index, champ in enumerate(player2):
        for real_champ in list_of_champions(sock):
            if champ == real_champ.name:
                player2[index] = real_champ
                
    # Match
    match = Match(
        Team(player1),
        Team(player2)
    )
    match.play()
    
    # Print a summary
    print_match_summary(match)
    

    
    