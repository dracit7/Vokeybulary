
import json
import random

#######################################################
# The main class
#######################################################

class Value():
  '''A value can be anything you like.'''

  def __init__(self, name, descs):
    '''
      `name`: the name of this value
      `descs`: a list of descriptions
    '''
    self.name = name
    self.descriptions = descs
  
  def addDesc(self, desc):
    '''Append a description `desc` to the value's desc list'''
    self.descriptions += [ desc ]
  
  def delDesc(self, i):
    '''Delete a description by its index `i`'''
    del self.descriptions[i]
  
  def getVal(self):
    '''return (`name`, `descs`)'''
    return (self.name, self.descriptions)
  
  def getName(self):
    '''return `name`'''
    return self.name
  
  def rename(self, name):
    '''Rename the value'''
    self.name = name

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
        jsonDict = json.loads(fileptr.read())
        for key in jsonDict:
          self.dbDict[key] = []
          for val in jsonDict[key]:
            name, descs = val
            self.dbDict[key] += [ Value(name, descs) ]
    except FileExistsError:
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

  def findVal(self, val):
    '''
      Find all matches of value in the database
    '''
    hitList = []
    for key in self.dbDict:
      for Value in self.dbDict[key]:
        value, descs = Value.getVal()
        if value == val:
          hitList += [ (key, descs) ]
    return hitList

  def randFind(self):
    '''
      Return a k-v pair at random.
    '''
    randkey = random.choice(list(self.dbDict))
    return (randkey, self.dbDict[randkey])

  def addVal(self, key, value):
    '''
      Add a new element to the value list.
      Return True when succeed, False elsewise.
    '''
    try:
      Val, descs = value
      # Reference
      for Key in self.dbDict:
        for val in self.dbDict[Key]:
          if Val == val.getName():
            if key in self.dbDict:
              self.dbDict[key] = self.dbDict[key] + [ val ]
            else:
              self.dbDict[key] = [ val ]
            return self.SUCCEED
      # New
      if key in self.dbDict:
        self.dbDict[key] = self.dbDict[key] + [ Value(Val, descs) ]
      else:
        self.dbDict[key] = [ Value(Val, descs) ]
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
          value, _ = self.dbDict[key][i].getVal()
          if val == value:
            self.dbDict[key][i].addDesc(desc)
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
        value, _ = self.dbDict[key][i].getVal()
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
          value, descs = self.dbDict[key][i].getVal()
          if val == value:
            if serial < len(descs):
              self.dbDict[key][i].delDesc(serial)
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
      for val in self.dbDict[key]:
        value, descs = val.getVal()
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
        value, desc = self.dbDict[key][i].getVal()
        if val == value:
          self.dbDict[key][i] = Value(newVal, desc)
          return self.SUCCEED
      return self.KEY_NO_VAL
    else:
      return self.NO_KEY
  
  def dump(self, filename = 'conf/db.json'):
    '''
      Dump the content of the db to a json file.
    '''
    dumpDict = {}
    for key in self.dbDict:
      dumpDict[key] = []
      for val in self.dbDict[key]:
        dumpDict[key] += [ val.getVal() ]
    cont = json.dumps(dumpDict)
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

  print(testDB.findVal("bounce"))

  testDB.dump()
