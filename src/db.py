
import json

#######################################################
# The main class
#######################################################

class Database():
  '''The Database used by the program'''

  dbDict = { } # key: string, value: list of string

  def __init__(self, dbFileName = "data/db.json"):
    '''
      Initialize the database by a specified json file.
    '''
    try:
      with open(dbFileName, "r") as fileptr:
        self.dbDict = json.loads(fileptr.read())
    except:
      exception(dbFileName + ": No such file or directory.")

  def find(self, key):
    '''
      Find the value of a kv-pair by key.
        - exist: return the corresponding value
        - non-exist: return *None*
    '''
    if key in self.dbDict:
      return self.dbDict[key]
    else:
      return None

  def addVal(self, key, value):
    '''
      Add a new element to the value list.
      Return True when succeed, False elsewise.
    '''
    try:
      if key in self.dbDict:
        if value not in self.dbDict[key]:
          self.dbDict[key] = self.dbDict[key] + [ value ]
      else:
        self.dbDict[key] = [ value ]
      return True
    except:
      return False

  def delKey(self, key):
    '''
      Delete a existing key. If the given key itself does not exist,
      this function just do nothing.
    '''
    if key in self.dbDict:
      del self.dbDict[key]
      return True
    else:
      return False
  
  def delVal(self, key, val):
    '''
      Delete an element from dbDict[key].
      If the given key or value does not exists, this function just do nothing.
    '''
    if key in self.dbDict:
      if val in self.dbDict[key]:
        self.dbDict[key].remove(val)
        if len(self.dbDict[key]) == 0:
          self.delKey(key)
        return True
    return False
  
  def List(self, log):
    '''
      List all keys and values in database.
    '''
    for key in self.dbDict:
      log(key + ':')
      for val in self.dbDict[key]:
        log("  " + val)

  
  def dump(self, filename = 'conf/db.json'):
    '''
      Dump the content of the db to a json file.
    '''
    cont = json.dumps(self.dbDict)
    with open(filename, "w") as fileptr:
      fileptr.write(cont)

#######################################################
# Functions
#######################################################

def exception(msg):
  print(msg)
  exit(0)

def error(msg):
  print("Error: " + msg)
  exit(1)

#######################################################
# Debugging
#######################################################

if __name__ == "__main__":
    
  testDB = Database()

  testDB.addVal("tester", "saltedfish")
  testDB.addVal("tester", "frozenfrog")

  testDB.delVal("tester", "miss")
  print(testDB.find("tester"))

  testDB.delVal("tester", "frozenfrog")
  print(testDB.find("tester"))

  testDB.delKey("tester")
  print(testDB.find("tester"))

  testDB.dump()
