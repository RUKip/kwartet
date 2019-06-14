class InputHandler(object):

    HELP_COMMAND = "help"
    SHOW_CARDS_COMMAND = "show cards"
    GIVE_ASK_OPTIONS_COMMAND = "give options"

    INVALID_INPUT_RESPONSE = "Sorry not valid"

   def handleIntInput(question, exceptions):
       answer = None
       while answer is None:
           try:
               answer = int(input(question))
               for exception in exceptions:
                   if (answer == exception):
                       raise Exception(exception)

                   if (not (agent_id in self.opponents)):
                   raise Exception("Available agents are: " + str(self.opponents.keys()))
           except:
               print(InputHandler.INVALID_INPUT_RESPONSE)
               agent_id = None

def defaultHandle(input):
        if(input == InputHandler.HELP_COMMAND):
            showPossibleCommands()


    def showPossibleCommands():
        print("Possible commands are:")
        print(InputHandler.SHOW_CARDS_COMMAND + ": " + "Output your current cards")
        print(InputHandler.GIVE_ASK_OPTIONS_COMMAND + ": " + "Give a set of card options you can ask")