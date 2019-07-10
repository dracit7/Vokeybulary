
import json

#######################################################
# The main class
#######################################################

class Database():
  '''The Database used by the program'''

  dbDict = { } # key: string, value: list of (string, list of string)

  # error codes
  SUCCEED = 0
  NO_KEY = 1
  KEY_NO_VAL = 2
  WRONG_TYPE = 3
  OUT_OF_RANGE = 4
  DUPLICATED = 5

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
        Val, _ = value
        for (val, _) in self.dbDict[key]:
          if Val == val:
            return self.DUPLICATED
        self.dbDict[key] = self.dbDict[key] + [ value ]
      else:
        self.dbDict[key] = [ value ]
      return self.SUCCEED
    except ValueError:
      return self.WRONG_TYPE
  
  def addDesc(self, key, val, desc):
    '''
      Add a new element to the description list of a value.
    '''
    try:
      if key in self.dbDict:
        for i in range(0, len(self.dbDict[key])):
          value, descs = self.dbDict[key][i]
          if val == value:
            self.dbDict[key][i] = (value, descs + [ desc ])
            return self.SUCCEED
        return self.KEY_NO_VAL
      return self.NO_KEY
    except ValueError:
      return self.WRONG_TYPE

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
    hasval = False

    if key in self.dbDict:
      for i in range(0, len(self.dbDict[key])):
        value, _ = self.dbDict[key][i]
        if val == value:
          del self.dbDict[key][i]
          hasval = True
          break
      if len(self.dbDict[key]) == 0:
        self.delKey(key)
      if hasval == False:
        return self.KEY_NO_VAL
      else:
        return self.SUCCEED
    else:
      return self.NO_KEY
  
  def delDesc(self, key, val, seri):
    '''
      Delete a description by its serial in desc list
    '''
    try:
      serial = int(seri)
      if key in self.dbDict:
        for i in range(0, len(self.dbDict[key])):
          value, descs = self.dbDict[key][i]
          if val == value:
            if serial < len(descs):
              del descs[serial]
              self.dbDict[key][i] = (value, descs)
              return self.SUCCEED
            else:
              return self.OUT_OF_RANGE
        return self.KEY_NO_VAL
      else:
        return self.NO_KEY
    except ValueError:
      return self.WRONG_TYPE
  

  
  def List(self, log):
    '''
      List all keys and values in database.
    '''
    for key in self.dbDict:
      log('<' + key + '>:')
      for (value, descs) in self.dbDict[key]:
        log("  <" + value + ">")
        if len(descs) == 0: 
          log("    No description yet")
        else:
          for desc in descs:
            log("    " + desc)
  
  def modVal(self, key, val, newVal):
    '''
      Modify a value to a new one.
    '''
    if key in self.dbDict:
      for i in range(0, len(self.dbDict[key])):
        value, desc = self.dbDict[key][i]
        if val == value:
          self.dbDict[key][i] = (newVal, desc)
          return self.SUCCEED
      return self.KEY_NO_VAL
    else:
      return self.NO_KEY
  
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
