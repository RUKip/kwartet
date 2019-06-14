import sys

HELP_COMMAND = "help"
EXIT_COMMAND = "exit"
SHOW_CARDS_COMMAND = "show cards"
GIVE_ASK_OPTIONS_COMMAND = "give options"

INVALID_INPUT_RESPONSE = "Sorry not valid"


def handleInput(question, type_cast=str, human_agent=None):
    answer = None
    while answer is None:
        try:
            answer = input(question)
            defaultHandle(answer, human_agent)
            answer = type_cast(answer)
        except:
            print(INVALID_INPUT_RESPONSE)
            answer = None
    return answer


def defaultHandle(input, humanAgent):
    if input == HELP_COMMAND:
        showPossibleCommands()
    if input == EXIT_COMMAND:
        sys.exit()

    if not (humanAgent is None):
        if input == SHOW_CARDS_COMMAND:
            humanAgent.showCardSet()
        if input == GIVE_ASK_OPTIONS_COMMAND:
            humanAgent.showAskOptions()


def showPossibleCommands():
    print("------------------------------------")
    print("Possible commands are:")
    print(EXIT_COMMAND + " => " + "When you are completely done with this game!")
    print(SHOW_CARDS_COMMAND + " => " + "Output your current cards")
    print(GIVE_ASK_OPTIONS_COMMAND + " => " + "Give a set of card options you can ask")
    print("------------------------------------")