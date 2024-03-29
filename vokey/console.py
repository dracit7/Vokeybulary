
import sys
import getopt
import pyfiglet

import database as db
import utils

# The console
class Console():
  '''
    A REPL-like console for vokeybulary
  '''

  def __init__(self, dbPath = 'vokey/data/db.json', histNum = 3):
    if histNum < 1:
      exception("Unsupported history number: "+str(histNum))
    self.dbPath = dbPath
    self.database = db.Database(dbPath)
    self.histNum = histNum
    self.histBuf = []
    for _ in range(0, histNum):
      self.histBuf += [""]

  def Start(self):
    '''
      Start the console.
    '''
    while True:
      command = input('>> ')
      print()
      if self.handle(command) == True:
        for i in range(0, self.histNum-1):
          i = self.histNum - i - 1
          self.histBuf[i] = self.histBuf[i-1]
        self.histBuf[0] = command # We do not record bad commands.
      print()
      self.database.dump(self.dbPath)
  
  def log(self, msg):
    '''
      Modify this if we need to log in other ways
    '''
    print(msg)
  
  def trim(self, lst):
    '''
      Trim a list to get rid of empty strings
    '''
    for i in range(0, len(lst)):
      if lst[i] == "":
        del lst[i]
        return self.trim(lst)
    return lst
  
  def handle(self, command):
    '''
      Execute the command specified by args.
    '''

    # Splict command into args
    if command == "":
      return False 
    args = command.split(" ")
    args = self.trim(args)

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
        self.log("Values corresponding to <" + utils.highlight(args[1], 33) + "> are:")
        for Val in reply:
          val, descs = Val.getVal()
          self.log("  <" + utils.highlight(val, 36) + ">")
          if len(descs) == 0:
            self.log("    No description yet")
          else:
            for desc in descs:
              self.log("    " + desc)
    
    # Find value
    elif args[0] == "findval" or args[0] == "fv":
      if len(args) != 2:
        self.fault(command)
        return False
      reply = self.database.findVal(args[1])
      if reply == []:
        self.log("No such value")
      else:
        self.log("There are " + utils.highlight(str(len(reply)), 32) + " hits in database:\n")
        for (key, descs) in reply:
          self.log("In <" + utils.highlight(key, 33) + ">:")
          if len(descs) == 0:
            self.log("  No descriptions yet")
          for desc in descs:
            self.log("  " + desc)
    
    elif args[0] == "match" or args[0] == "m":
      if len(args) != 2:
        self.fault(command)
        return False
      reply = self.database.fuzzyFind(args[1])
      if reply == []:
        self.log("No matches")
      else:
        self.log("There are " + str(len(reply)) + " hits in database:\n")
        for result in reply:
          self.log(result+"\n")
 
    
    # Test
    elif args[0] == "test" or args[0] == "t":
      # Get a quiz at random
      if len(args) != 1:
        self.fault(command)
        return False
      key, values = self.database.randFind()
      # Print the quiz
      self.log("Key: <" + utils.highlight(key, 33) + ">")
      self.log("Can you remember its values? There are " + utils.highlight(str(len(values)), 32) + " values in all.\n")
      # Answer the quiz
      leftcnt = len(values)          # number of unanswered values
      trycnt = 0                     # number of answers in total
      correctcnt = 0                 # number of correct answers
      face = utils.highlight("('v') ", 32) # this face represents true or false
      while True:
        if leftcnt == 0:
          self.log("All answered! Congratulations :)")
          break
        answer = input(face)
        if answer == "quit" or answer == "q":
          self.log("That's fine. here're answers...")
          break
        trycnt += 1
        face = "Missed.\n"+utils.highlight("(>_<) ", 31)
        for Val in values:
          value, _ = Val.getVal()
          if answer == value:
            leftcnt -= 1
            self.log("Correct!")
            correctcnt += 1
            face = utils.highlight("('v') ", 32)
      # Show answer
      self.log("\n You have tried " + utils.highlight(str(trycnt), 32) + " times")
      self.log(" " + utils.highlight(str(correctcnt), 32) + " of them are correct.")
      self.log("\n<" + utils.highlight(key, 33) + ">:")
      for Val in values:
        value, descs = Val.getVal()
        self.log("  <" + utils.highlight(value, 36) + ">")
        if len(descs) == 0:
          self.log("    No description yet")
        for desc in descs:
          self.log("    " + desc)
      return False # do not record this
      

    # Add
    elif args[0] == "add" or args[0] == "a":
      # Add a value
      if len(args) == 3:
        reply = self.database.addVal(args[1], (args[2], []))
        if reply == self.database.WRONG_TYPE:
          self.log(utils.highlight("Error: invalid data type.", 31))
          return False
        elif reply == self.database.DUPLICATED:
          self.log("This value is already in the database")
        else:
          self.log(utils.highlight("Succeed", 32))
      # Add a description
      elif len(args) == 4:
        reply = self.database.addDesc(args[1], args[2], args[3])
        if reply == self.database.WRONG_TYPE:
          self.log(utils.highlight("Error: invalid data type.", 31))
          return False
        elif reply == self.database.NO_KEY:
          self.log("No such key")
        elif reply == self.database.KEY_NO_VAL:
          self.log("This key does not map to such value")
        else:
          self.log(utils.highlight("Succeed", 32))
      else:
        self.fault(command)
        return False
    
    # Add by value
    elif args[0] == "addbyvalue" or args[0] == "abv" or args[0] == "av":
      if len(args) != 3:
        self.fault(command)
        return False
      reply = self.database.findVal(args[1])
      if len(reply) == 0:
        self.log("No such value")
      elif len(reply) > 1:
        self.log("More than one value existing, please merge conflict first")
      else:
        key, _ = reply[0]
        reply = self.database.addDesc(key, args[1], args[2])
        if reply == self.database.WRONG_TYPE:
          self.log(utils.highlight("Error: invalid data type.", 31))
          return False
        elif reply == self.database.NO_KEY:
          self.log("No such key")
        elif reply == self.database.KEY_NO_VAL:
          self.log("This key does not map to such value")
        else:
          self.log(utils.highlight("Succeed", 32)) 

    # Delete
    elif args[0] == "delete" or args[0] == "del" or args[0] == "d":
      # Delete key
      if len(args) == 2:
        if self.database.delKey(args[1]) == False:
          self.log("No such key")
        else:
          self.log(utils.highlight("Succeed", 32))
      # Delete value
      elif len(args) == 3:
        err = self.database.delVal(args[1], args[2])
        if err == self.database.NO_KEY:
          self.log("No such key")
        elif err == self.database.KEY_NO_VAL:
          self.log("This key does not map to such value")
        else:
          self.log(utils.highlight("Succeed", 32))
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
          self.log(utils.highlight("Succeed", 32))
      else:
        self.fault(command)
        return False
    
    # List
    elif args[0] == "list" or args[0] == "ls" or args[0] == "l":
      if len(args) == 1:
        self.database.List(self.log)
      elif len(args) == 2:
        if args[1] == "history" or args[1] == "hist" or args[1] == "h":
          for i in range(0, self.histNum):
            i = self.histNum - i - 1
            if self.histBuf[i] == "":
              self.log("History "+str(i+1)+": None")
            else:
              self.log("History "+str(i+1)+": "+self.histBuf[i])
        else:
          self.fault(command)
      else:
        self.fault(command)
      return False # Do not record list operations
    
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
          self.log(utils.highlight("Succeed", 32))
      else:
        self.fault(command)
        return False
    
    # Help
    elif args[0] == "help" or args[0] == "h":
      if len(args) == 1:
        utils.helper()
      elif len(args) == 2:
        utils.helper(args[1])
      else:
        self.fault(command)
      return False # do not record `help` into command-history

    # History
    elif args[0] == "history" or args[0] == "hist":
      if len(args) < 1:
        self.fault(command)
        return False
      elif len(args) == 1:
        self.handle(self.histBuf[0])
        return False
      else:
        argv = self.histBuf[0].split(" ")
        newCommand = ""
        for i in range(0, len(argv) - len(args) + 1):
          newCommand += argv[i] + " "
        for i in range(1, len(args)):
          newCommand += args[i] + " "
        self.log("Hist-operation: " + newCommand + "\n")
        self.handle(newCommand)
        return False
    elif args[0][0] == "h":
      for i in range(0, self.histNum):
        if args[0] == "h"+str(i+1):
          if len(args) < 1:
            self.fault(command)
            return False
          elif len(args) == 1:
            self.handle(self.histBuf[i])
            return False
          else:
            argv = self.histBuf[i].split(" ")
            newCommand = ""
            for i in range(0, len(argv) - len(args) + 1):
              newCommand += argv[i] + " "
            for i in range(1, len(args)):
              newCommand += args[i] + " "
            self.log("Hist-operation: " + newCommand + "\n")
            self.handle(newCommand) 
            return False
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
  
  path = "vokey/data/db.json"

  # Parse options
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:m:", ["database=", "merge=", "help"])
  except:
    # Wrong usage, throw an error
    error("Invalid arguments. Use -h or --help to see usage.")
  
  for (opt, value) in opts:
    if opt == "-d" or opt == "--database":
      path = value
    if opt == "-m" or opt == "--merge":
      utils.mergeFile(path, value)
      exit(0)
    if opt == "-h" or opt == "--help":
      print('''
Usage: python3 main.py [-h] [-d PATH]

Options:

  -h              Display this help
  -d PATH         Specify the path of the database file("data/db.json" by default)

''')
      exit(0)

  # Show the user interface
  pyfiglet.print_figlet("Vokeybulary", font="chunky", colors=":")

  # Start the console
  console = Console(path)
  console.Start()
  
