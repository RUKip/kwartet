import logging

from Game import Game

# delete filemode = 'w' to append log to previous run
# with this format='%(message)s' to write messages without the INFO:root:
# logging.basicConfig(filename='output.log', filemode='w', level=logging.DEBUG, format='%(message)s')

logging.basicConfig(filename='output.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(asctime)s -  %(levelname)s - %(message)s')


logging.info("Starting simulation")
icon = """
          _____
         |A .  | _____
         | /.\ ||A ^  | _____
         |(_._)|| / \ ||A _  | _____
         |  |  || \ / || ( ) ||A_ _ |
         |____V||  .  ||(_'_)||( v )|
                |____V||  |  || \ / |
                       |____V||  .  |
                              |____V|
"""
logging.info(icon)
game = Game()
game.initGame()
game.startGame()

