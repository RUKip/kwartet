import logging

from Game import Game

"""Print nice Logo and Title"""
f = open("output.log", 'w')
title = """Simulation of simplified version of the well known Kwartet game.

          _____
         |A .  | _____
         | /.\ ||A ^  | _____
         |(_._)|| / \ ||A _  | _____
         |  |  || \ / || ( ) ||A_ _ |
         |____V||  .  ||(_'_)||( v )|
                |____V||  |  || \ / |
                       |____V||  .  |
                              |____V|


Done by Diego Cabo, Tanja de Vries and Ruben Kip\n"""
f.write(title)
f.write("\n---------------------------------------------------------------\n\n")
f.close()

# delete filemode = 'w' to append log to previous run
# with this format='%(message)s' to write messages without the <time> INFO:root:
# logging.basicConfig(filename='output.log', filemode='w', level=logging.DEBUG, format='%(message)s')
logging.basicConfig(filename='output.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(message)s')
# format='%(asctime)s -  %(levelname)s - %(message)s') # to print INFO or DEBUG


# define a Handler which writes WARNING messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)
logging.info("Starting simulation")

# set number of players
player_cnt = 5
while player_cnt is None:
    try:
        player_cnt = int(input("How many players?: "))
        if(player_cnt<1):
            print("Too small player count!")
            player_cnt = None
    except:
        print("Not valid, try a different number")
        pass

# set number of games played
games_cnt = 1
while games_cnt is None:
    try:
        games_cnt = int(input("How many games?: "))
        if(games_cnt<1):
            print("Too small games count!")
            games_cnt = None
    except:
        print("Not valid, try a different number")
        pass

final_result = [0] * (player_cnt+1)

for i in range (1,games_cnt+1):
    game = Game()
    game.initGame(player_cnt)
    result = game.startGame()
    
    for x in range (1, player_cnt+1):
        final_result[x] += result[x]

for x in range (1, player_cnt+1):
    print(("Player %d: " %x) + str(final_result[x]/games_cnt))

