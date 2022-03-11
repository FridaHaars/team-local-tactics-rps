from time import sleep as sleep
from player import get_players
from rich.table import Table
from rich import print
from champion import list_of_player_champnames
from client import request



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''                         Main gameplay simulation.                            '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


'''
Loads the following from various files:
1. The current champion selection from each player
2. The "rolls" of each player, which is generated right after they choose their champions.
3. The styles of the players themselves, so that they look presentable during combat :)
'''
def play() -> None:
    '''
    We need players to play!
    '''
    player1, player2 = get_players()
    
    
    '''
    Reference dict for emojis to display instead of "rock", "paper", or "scissors"
    
    Because just showing text is soooo inf100 ;ppPPPppPPppP
    '''
    emojis = {
        'r' : ':raised_fist-emoji:',
        'p' : ':raised_hand-emoji:',
        's' : ':victory_hand-emoji:'}  #type and matching aesthetics
    
    
    
    '''
    Simple map logic which decides what beats what!
    '''
    win_combos = {'r' : 's',           #rock beats scissors
                  'p' : 'r',           #paper beats rock
                  's' : 'p'}           #scissors beats paper



    '''
    We get the rolls in condensed string format, such as "rrpssp" which would be rock,rock,paper,scissors,scissors,paper
    '''
    player1_champs, player2_champs = list_of_player_champnames(1),  list_of_player_champnames(2) 
    player1_rolls, player2_rolls = request.to_server("from_db=get_rolls=").split('+')
    ''''''
    

    '''
    Prints out a dramatic countdown, just for fun
    '''
    print_dramatic_text()
    ''''''
    
    
    '''
    Start playing one game consisting of three rounds of two rolls each!
    '''
    player1_score, player2_score = 0,0
    round, roll = 0, 0
    while round < 3:
        '''
        One round gets one table
        '''
        round_summary = Table(title=f'Round {round+1}')

        '''
        Creates two columns in that table, one for each player
        '''
        round_summary.add_column(player1.name,style=player1.color, no_wrap=True , justify="center")
        round_summary.add_column(player2.name, style=player2.color, no_wrap=True, justify="center")
        
        '''
        Each round consists of two rolls, which we add to the table with their corresponding emoji
        '''
        for _ in range (0, 2):
            round_summary.add_row(f"{player1_champs[_]}  {emojis[player1_rolls[roll]]}",
                                f"{player2_champs[_]}  {emojis[player2_rolls[roll]]}")
            
            '''
            Declares the winner according to the wincombos dictionary.
            '''
            if player1_rolls[roll] == win_combos[player2_rolls[roll]]:
                player2.score += 1
            elif player2_rolls[roll] == win_combos[player1_rolls[roll]]:
                player1.score += 1
            roll += 1
        
        '''
        Prints the summary of the round, and sleeps briefly to build suspense!
        '''
        print(round_summary)
        print('\n')
        round += 1
        sleep(0.75)


    '''
    Prints out the score in pretty colors
    '''
    print(f'[bold yellow]FINAL SCORE[/bold yellow]\n'
          f'[{player1.color}]{player1.name}:[/{player1.color}]'
          f'[bold]{player1.score}[/bold]\n'
          f'[{player2.color}]{player2.name}:[/{player2.color}]'
          f'[bold]{player2.score}[/bold]')
    
    
    '''
    The winner is declared!
    '''
    if player1.score > player2.score:
        print(f'\n[{player1.color}]{player1.name} wins! :grin:')
    elif player1.score < player2.score:
        print(f'\n[{player2.color}]{player2.name} wins! :grin:')
    else:
        print("\nIt's a draw :expressionless:")
    
    
    '''
    The winner gets to bask in glory for a whole two seconds!
    '''
    sleep(1)
    print("[italic yellow]Returning players to the lobby...[/italic yellow]")
    sleep(1)
    
  
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  
  
  
  
  
'''
Collects our ascii-art logo from a text file in the database
'''
def print_logo():
    part1, part2 = request.to_server("from_db=get_logo=").split('+')
    print(part1)
    sleep(0.75)
    print(part2)
    print("[italic yellow]\nThe game will begin shortly.[/italic yellow]")
    sleep(2.5)
    print("\n")
     
       
'''
Dramatic countdown function to be called during battles.
'''
def print_dramatic_text():
    print("\n\n")
    sleep(0.25)
    print(f"[italic yellow]All set! Champions, prepare yourselves to battle in...[/italic yellow]")
    sleep(0.25)
    print("3...")
    sleep(0.75)
    print("2...")
    sleep(0.75)
    print("1...")
    sleep(0.75)
    print(f"[bold yellow]Go![/bold yellow]")
    print()
    sleep(0.25)
    