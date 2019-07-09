
import sys
import getopt
import pyfiglet

# We imports library files from ./src folder
sys.path.append("src")

from db import *

# The console
class Console():
  '''
    A REPL-like console for vokeybulary
  '''

  def __init__(self, dbPath = 'data/db.json'):
    self.dbPath = dbPath
    self.database = Database(dbPath)

  def Start(self):
    '''
      Start the console.
    '''
    while True:
      command = input('>> ')
      if self.handle(command) == True:
        print('o', end='')
      else:
        print('x', end='')
      self.database.dump(self.dbPath)
  
  def log(self, msg):
    '''
      Modify this if we need to log in other ways
    '''
    print(msg)
  
  def handle(self, command):
    '''
      Execute the command specified by args.
    '''
    args = command.split(" ")

    if args[0] == "find" or args[0] == "f":
      if len(args) != 2:
        self.fault(command)
        return False
      reply = self.database.find(args[1])
      if reply == None:
        self.log("No such key")
      else:
        self.log("Values corresponding to " + args[1] + " are:")
        for val in reply:
          self.log("\t" + val)

    elif args[0] == "add" or args[0] == "a":
      if len(args) != 3:
        self.fault(command)
        return False
      reply = self.database.addVal(args[1], args[2])
      if reply == False:
        self.log("Error: invalid data type.")
        return False

    elif args[0] == "del" or args[0] == "d":
      if len(args) == 2:
        if self.database.delKey(args[1]) == False:
          self.log("No such key")
      elif len(args) == 3:
        if self.database.delVal(args[1], args[2]) == False:
          self.log("No such key or this key does not map to such value")
      else:
        self.fault(command)
        return False
    
    elif args[0] == "list" or args[0] == "ls" or args[0] == "l":
      if len(args) != 1:
        self.fault(command)
      self.database.List(self.log)

    elif args[0] == "quit" or args[0] == "exit" or args[0] == "q":
      exit(0)

    else:
      self.fault(command)
      return False

    return True
        
  
  def fault(self, opeName):
    '''
      Print a string indicating the wrong usage of a command.
    '''
    self.log("Wrong usage: " + opeName + "\nYou may use 'help' to get the right usage.")
        
if __name__ == "__main__":
  
  # Parse options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:", ["database=", "help"])
  except:
    # Wrong usage, throw an error
    error("Invalid arguments. Use -h or --help to see usage.")

  # Show the user interface
  pyfiglet.print_figlet("Vokeybulary", font="chunky", colors=":")

  # Start the console
  console = Console()
  console.Start()
  