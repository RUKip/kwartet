import logging
import time

import InputHandler
from Game import Game


def list_of_zeroes(n):
	return [0] * n


def ask_player_cnt():
	while True:
		player_cnt = InputHandler.handleInput("How many players?: ", type_cast=int)
		if player_cnt < 1:
			print("Too small player count!")
		else:
			break
	return player_cnt


def ask_game_cnt():
	while True:
		games_cnt = InputHandler.handleInput("How many games?: ", type_cast=int)
		if games_cnt < 1:
			print("Too small games count!")
		else:
			break
	return games_cnt

def ask_multiple_games():
	while True:
		answer = InputHandler.handleInput("Do you want to play multiple games? (y/n): ")
		if answer[0] == "y":
			games_cnt = ask_game_cnt()
			break
		elif answer[0] == "n":
			games_cnt = 1
			break
		else:
			print("Try again, the y and n are located in the middle area of the keyboard...")
	return games_cnt

def ask_human_player(player_cnt):
	while True:
		answer = InputHandler.handleInput("Do you want to join the fun? Note: no UI availble (y/n)")
		if answer[0] == "y":
			print("Cool, you will be player " + str(player_cnt))
			return True
		else:
			print("Ok guess not")
			return False

def start_one_game(player_cnt, has_human_player):
	print("Lets rumble!.. (This can take a few sec)")
	game = Game(has_human_player)
	game.initGame(player_cnt)
	result = game.startGameLoop()
	return result


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


Created by Diego Cabo, Tanja de Vries and Ruben Kip\n"""
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
# player_cnt = 3
player_cnt = ask_player_cnt()

has_human_player = ask_human_player(player_cnt)

if has_human_player:
	print("Tip: use the 'help' command to ` see all available commands")
	time.sleep(3)
	result = start_one_game(player_cnt, has_human_player)
	if result[player_cnt] == max(result.values()):
		print("You win, congrats!")
	else:
		print("You lose!, don't worry they have a very good memory")
	print("final score: " + str(result))
else:
	# set number of games played
	# games_cnt = 1
	games_cnt = ask_multiple_games()

	final_result = list_of_zeroes(player_cnt + 1)
	for i in range(1, games_cnt + 1):
		result = start_one_game(player_cnt, has_human_player)

		#single winner function
		winner = max(result, key=result.get)
		final_result[winner] += 1

	''' Second place still loses! Commented this count to see which players actually win games	
		for x in range (1, player_cnt+1):
			final_result[x] += result[x]
	'''

	for x in range(1, player_cnt + 1):
		print(("Percentage won player %d: " % x) + str((final_result[x] / games_cnt) *100))
