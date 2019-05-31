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
                    format='%(asctime)s -  %(levelname)s - %(message)s')


# define a Handler which writes WARNING messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)
logging.info("Starting simulation")

game = Game()
game.initGame()
game.startGame()

