import logging
import time

import InputHandler
from ComputerAgent import ComputerAgent
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


def ask_set_strategies(nr_of_players):
	while True:
		answer = InputHandler.handleInput("Set specific agent strategies? (y/n): ")
		if answer[0] == "y":
			(logic, thinking) = ask_strategies(nr_of_players)
			break
		elif answer[0] == "n":
			logic = {x:ComputerAgent.STRATEGY_1ST for x in range(1, nr_of_players+1)}	#default everyone plays 1st order logic
			thinking = {x:ComputerAgent.BASIC_THINKING for x in range(1, nr_of_players+1)} #default everyone plays with basic thinking
			break
		else:
			print("Try again, the y and n are located in the middle area of the keyboard...")
	return logic, thinking

def ask_strategies(nr_of_players):
	print("Please no faulty input here")
	#ask logic order
	logic = {x: ComputerAgent.STRATEGY_RANDOM for x in range(1, nr_of_players+1)}
	answer = input("Who plays 1st order? (example syntax: 1,3,4): ")
	first_players = list(map(int,answer.split(",")))
	for first_player in first_players:
		logic[first_player] = ComputerAgent.STRATEGY_1ST

	answer = input("Who plays 2nd order? (example syntax: 1,3,4): ")
	second_players = list(map(int,answer.split(",")))
	for second_player in second_players:
		logic[second_player] = ComputerAgent.STRATEGY_2ND
	print("Everyone else plays random!")

	#ask thinking strategy
	thinking = {x: ComputerAgent.BASIC_THINKING for x in range(1, nr_of_players+1)}
	answer = input("Who do advanced thinking? (example syntax: 1,2,4): ")
	smarty_pants = list(map(int, answer.split(",")))
	for advanced_player in smarty_pants:
		thinking[advanced_player] = ComputerAgent.ADVANCED_THINKING
	print("Everyone else just basic!")

	return logic, thinking



def ask_human_player(nr_of_players):
	while True:
		answer = InputHandler.handleInput("Do you want to join the fun? Note: no UI availble (y/n)")
		if answer[0] == "y":
			print("Cool, you will be player " + str(nr_of_players))
			return True
		else:
			print("Ok guess not")
			return False


def start_one_game(nr_of_players, has_human_player, logic, thinking):
	print("Lets rumble!.. (This can take a few sec)")
	game = Game(has_human_player, thinking)
	game.initGame(nr_of_players, logic)
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

logic, thinking = ask_set_strategies(player_cnt)

has_human_player = ask_human_player(player_cnt)

if has_human_player:
	print("Tip: use the 'help' command to see all available commands")
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
		result = start_one_game(player_cnt, has_human_player, logic, thinking)

		#single winner function, on case of draw divide the win
		winner_count = 0
		winners = []
		max_value = max(result.values())
		for agent_nr in range(1, player_cnt + 1):
			if result[agent_nr] == max_value:
				winner_count+=1
				winners.append(agent_nr)

		if winner_count>1:
			print("There was a draw!, winners: " + str(winners))

		for winner in winners:
			final_result[winner] += 1/winner_count

	''' Second place still loses! Commented this count to see which players actually win games	
		for x in range (1, player_cnt+1):
			final_result[x] += result[x]
	'''

	for x in range(1, player_cnt + 1):
		print(("Percentage won player %d: " % x) + str((final_result[x] / games_cnt) *100))
