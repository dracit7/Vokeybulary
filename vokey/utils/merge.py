
import json

targetDB = {}
srcDB = {}

def mergeFile(target, src):
  try:
    with open(src, "r") as srcptr:
      srcDB = json.loads(srcptr.read())
    with open(target, "r") as targetptr:
      targetDB = json.loads(targetptr.read())
    with open(target, "w") as fileptr:
      for key in srcDB:
        if key not in targetDB:
          targetDB[key] = srcDB[key]
      fileptr.write(json.dumps(targetDB))
    print("Merge completed")
  except FileNotFoundError:
    exception("No such file or directory.")
