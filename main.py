
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
      print()
      if self.handle(command) == True:
        print()
        print('o', end='')
      else:
        print()
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

    # Splict command into args
    if command == "":
      return True
    args = command.split(" ")

    # Find
    if args[0] == "find" or args[0] == "f":
      # Validity check
      if len(args) != 2:
        self.fault(command)
        return False
      # Query
      reply = self.database.find(args[1])
      # Parse the reply
      if reply == None:
        self.log("No such key")
      else:
        self.log("Values corresponding to <" + args[1] + "> are:")
        for (val, descs) in reply:
          self.log("  <" + val + ">")
          if len(descs) == 0:
            self.log("    No description yet")
          else:
            for desc in descs:
              self.log("    " + desc)

    # Add
    elif args[0] == "add" or args[0] == "a":
      # Add a value
      if len(args) == 3:
        reply = self.database.addVal(args[1], (args[2], []))
        if reply == self.database.WRONG_TYPE:
          self.log("Error: invalid data type.")
          return False
        elif reply == self.database.DUPLICATED:
          self.log("This value is already in the database")
        else:
          self.log("Succeed")
      # Add a description
      elif len(args) == 4:
        reply = self.database.addDesc(args[1], args[2], args[3])
        if reply == self.database.WRONG_TYPE:
          self.log("Error: invalid data type.")
          return False
        elif reply == self.database.NO_KEY:
          self.log("No such key")
        elif reply == self.database.KEY_NO_VAL:
          self.log("This key does not map to such value")
        else:
          self.log("Succeed")
      else:
        self.fault(command)
        return False

    # Delete
    elif args[0] == "delete" or args[0] == "del" or args[0] == "d":
      # Delete key
      if len(args) == 2:
        if self.database.delKey(args[1]) == False:
          self.log("No such key")
        else:
          self.log("Succeed")
      # Delete value
      elif len(args) == 3:
        err = self.database.delVal(args[1], args[2])
        if err == self.database.NO_KEY:
          self.log("No such key")
        elif err == self.database.KEY_NO_VAL:
          self.log("This key does not map to such value")
        else:
          self.log("Succeed")
      # Delete description
      elif len(args) == 4:
        err = self.database.delDesc(args[1], args[2], args[3])
        if err == self.database.NO_KEY:
          self.log("No such key")
        elif err == self.database.KEY_NO_VAL:
          self.log("This key does not map to such value")
        elif err == self.database.OUT_OF_RANGE:
          self.log("The index provided is out of range")
        elif err == self.database.WRONG_TYPE:
          self.log("The serial must be int")
        else:
          self.log("Succeed")
      else:
        self.fault(command)
        return False
    
    # List
    elif args[0] == "list" or args[0] == "ls" or args[0] == "l":
      if len(args) != 1:
        self.fault(command)
        return False
      self.database.List(self.log)
    
    # Set
    elif args[0] == "set" or args[0] == "s":
      if len(args) < 2:
        self.fault(command)
        return False
      # Set value
      if args[1] == "value" or args[1] == "val" or args[1] == "v":
        if len(args) != 5:
          self.fault(command)
          return False
        err = self.database.modVal(args[2], args[3], args[4])
        if err == self.database.NO_KEY:
          self.log("No such key")
        elif err == self.database.KEY_NO_VAL:
          self.log("This key does not map to such value")
        else:
          self.log("Succeed")
      else:
        self.fault(command)
        return False

    # Exit
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
  