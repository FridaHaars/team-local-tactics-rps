from client import request
from player import Player, get_players, set_player_style
from game import play
from champion import *
from rich.prompt import Prompt
from rich.table import Table
from rich import print
from time import sleep


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''                         The following functions are all connected to eachother:                                        '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


"""
Verifies the user ID in the server so we can distinguish between two different players running the same client file
"""
def get_current_id():
    return request.to_server("check_id=")



'''
There is a counter inside the server which is incremented whenever a player makes a selection, and all even numbers mean player 1's turn.
This was a dumb idea but it kind of worked.
'''
def player1_turn() -> bool:
    return int(request.to_server("get_scount=")) % 2 == 0



'''
Players make their selections, and they wait while the other person is choosing using the validation function player1_turn using
the serverside counter. As you can see, when it's not their turn, players are stuck in a while loop!

At the end of this function, both players have decided their two champions, and we call "set_rolls",
This simulates the weapon selection of each champion based on their probabilities to do so. See dbreader.py for more info.
'''
def champion_selection():
    player1, player2 = get_players()
    
    while True:
        if get_current_id() == "1":
            input_champ(player1)
            request.to_server("inc_scount=")
            
            if not player1_turn():
                print(f"[italic yellow]Waiting for {player2.name}...[/italic yellow]")
                while not player1_turn():
                    continue
        
        elif (get_current_id()) == "2":
            if player1_turn():
                print(f"[italic yellow]Waiting for {player1.name}...[/italic yellow]")
                while player1_turn():
                    continue
            input_champ(player2)
            request.to_server("inc_scount=")
        
        if int(request.to_server("get_scount=")) == 4:
            if get_current_id() == "1":
                request.to_server("set_rolls=")
            break
 
    
'''
Helper method which asks a repeated prompt to the given player and validates the input.
'''
def input_champ(player : Player) -> None:
    
    #complimentary events
    other_id = 2 if player.id == 1 else 1
    
    
    #player-specific lists to know which player there might be a conflict with
    active_champlist = list_of_player_champnames(player.id)
    other_champlist = list_of_player_champnames(other_id)
    
    #creates an easy-access list of ALL champion names as a general reference
    list_of_all_champ_names = get_all_names()
    
    
    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        match Prompt.ask(f'[{player.color}]Select your champion[/{player.color}]'):
            case name if name not in list_of_all_champ_names:
                print(f'The champion {name} is not available. Try again.')
            case name if name in active_champlist:
                print(f'{name} is already in your team. Try again.')
            case name if name in other_champlist:
                print(f'{name} is in the enemy team. Try again.')
            case _:
                save_to_player_selection(object_from_name(name))
                break

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''                                                  END                                                                   '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''





'''
Add a champion to the main 'champions.csv' database

Validates input of the name and probabilities, if they are valid we convert the user input
to a "champion string" name,prob,prob,prob and save it by making a request to the server.
'''
def menu_add_champ() -> None:
    
    while True:
        name = input("Enter champion name: ")
        if len(name) > 20:
            print(error_message("Could not name champion!", "Name is too long."))
        elif not name:
            print(error_message("Could not name champion!", "No name given"))
        elif name in get_all_names():
            print(error_message("Could not name champion!", "Name already taken!"))
        elif name == "None":
            print(error_message("Could not name champion!", "Invalid name."))
        else:
            break

    total_prob = 0.0
    while True:
        try:
            rprob = float(input("Enter rock probability (0.0 - 1.0): "))
            pprob = float(input("Enter paper probability(0.0 - 1.0: "))
            sprob = float(input("Enter scissors probability(0.0 - 1.0): "))
        except:
            print(error_message("Could not assign probabilities to champion.", "Invalid format given!"))
        finally:  
            if float(rprob)+float(pprob)+float(sprob) == 1.0:
                break
            else:
                print(error_message("Could not assign probabilities to champion.", "Sum of probabilities not equal to 1.0!"))
            
            

    if len(get_all_names()) > 24:
        print(error_message(f"Failed to register champion {name}", "There are too many champions in the roster"))
    else:
        save_to_roster(string_to_object(f'{name},{rprob},{pprob},{sprob}'))
    


'''
Delete a champion from the main 'champions.csv' database

Input is validated to make sure the champion exists and that we are not deleting too many champions, rendering the game unplayable.
'''
def menu_delete_champ() -> None:
    champname, cancel = '', False
    
    list_of_champnames = get_all_names()
    
    print('[italic yellow]If you entered this menu by mistake, enter "cancel" to go back![/italic yellow]')
    while champname not in list_of_champnames:
        champname = input("Enter the precise name of the champion: ")
        if champname == "cancel":
            cancel = True
            break
        elif champname not in list_of_champnames:
            print(error_message(f"Failed to delete {champname}", "Champion not in roster! Check your spelling."))  
    
    if cancel:
        pass
    elif len(list_of_champnames) < 5:
        print(error_message(f"Failed to delete {champname}", "Champion roster is too small!"))
    else:
        delete_from_roster(champname)
        



'''
Collects champions from the 'champions.csv' database and prints it out in a nice format :)
'''
def menu_print_champs():

    # Create a table containing available champions
    available_champs = Table(title="Current roster:")

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    
    # Populate the table
    for champion in get_all():
        available_champs.add_row(*champion.str_tuple)
    available_champs.add_row()
    print()
    print(available_champs)
    
    

'''
Lets the current client change their player profile, changing their name and color.
This is bad code, but it was giving me problems and I am too lazy to fix it.
'''
def menu_change_style() -> None:
    while len(name:=input("Choose your new name: ")) not in range(1, 21):
        print(error_message(f"Failed to regiser {name}", "Name is either too long, or too short."))
    
    #workaround, sorry, it's ugly
    color = ''
    while color.lower() not in ['red', 'yellow', 'green', 'blue', 'indigo', 'purple']:
        color = input("Choose a color: ")
        if color.lower() not in ['red', 'yellow', 'green', 'blue', 'indigo', 'purple']:
            print(error_message(f"Failed to register color {color}", "Given color is not valid or is misspelled."))
    
    set_player_style(name, color.lower())

   

'''
The menu that actually lets you play, might be useful!

Resets the server-side counter and calls relevant functions which simulate gameplay:
1. Restarts in-game counters and removes previous player selections and rolls
2. Prints out a list of champions to choose from as a reference while the players are choosing
3. Let's the players choose their champions
4. Simulates a match and prints out the result!

After this has happened, the main gameplay portion is over.
'''
def menu_play():
    request.to_server("restart=")
    menu_print_champs()
    champion_selection()
    play()
   
   
   
   
'''
We have no plans to implement these functions
'''
def menu_view_history():
     print("This function is not yet implemented, sorry!")
    
    
def menu_clear_history():
    print("This function is not yet implemented, sorry!")
    



'''
Saves code and looks good, hehe
'''
def error_message(what_happened : str, the_reason_it_happend : str):
            return f"\n[italic yellow]{what_happened}![/italic yellow]\n[bold red]ERROR:[/bold red] [red]{the_reason_it_happend}[/red]\n"



'''
Simple table-based display menu, no functional purpose
'''
def get_menu() -> Table:
    table = Table(title="Choose wisely:")
    table.add_column("ID", justify="center")
    table.add_column(justify="center")
    table.add_column("Description", justify="center")
    table.add_row("[bold red]1[/bold red]",
                  "Play a game",
                  "[italic yellow]Go to the arena to battle.[/italic yellow]")
    table.add_row()
    table.add_row("[bold red]2[/bold red]",
                  "View champions",
                  "[italic yellow]Inspect current available roster.[/italic yellow]")
    table.add_row()
    table.add_row("[bold red]3[/bold red]",
                  "Add champion",
                  "[italic yellow]Add another champion to the roster.[/italic yellow]")
    table.add_row()
    table.add_row("[bold red]4[/bold red]",
                  "Remove champion",
                  "[italic yellow]Remove a champion from the roster.[/italic yellow]")
    table.add_row()
    table.add_row("[bold red]5[/bold red]",
                  "Change style",
                  "[italic yellow]Alter name and profile color.[/italic yellow]")
    table.add_row()
    table.add_row("[bold red]6[/bold red]",
                  "View history",
                  "[italic yellow]Inspect historic battles.[/italic yellow]")
    table.add_row()
    table.add_row("[bold red]7[/bold red]",
                  "Clear history",
                  "[italic yellow]Empty the archives.[/italic yellow]")
    table.add_row()
    table.add_row("[bold red]8[/bold red]",
                  "Exit",
                  "[italic yellow]Break current session.[/italic yellow]")
    return table
    



'''
This is the actual menu!

The player chooses an ID according to the table above, which is validated.

Then according to the id they enter, we send them to the appropriate menu.
'''    
def select_screen():
    print("\n\n")
    print(get_menu())
    
    while True:
        try:
            choice = int(input("Enter an ID: "))
        except:
            print("[italic red]Invalid ID![/italic red]")
        finally:
            if choice not in range(1, 9):
                print("[italic red]Invalid ID![/italic red]")
            else:
                break
                
    print("[italic yellow]Hold on...[/italic yellow]\n")
    sleep(0.5)
        
        
    if choice == 1:
        menu_play()
    elif choice == 2:
        menu_print_champs()
        print("[italic yellow]Hit 'Enter' when you're ready to proceed...[/italic yellow]")
        input()
    elif choice == 3:
        menu_add_champ()
    elif choice == 4:
        menu_print_champs()
        menu_delete_champ()
    elif choice == 5:
        menu_change_style()
    elif choice == 6:
        menu_view_history()
    elif choice == 7:
        menu_clear_history()
    elif choice == 8:
        exit()
    else:
        print("Something went wrong.")
        