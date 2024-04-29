
import os
import sys

def runCmd(cmdStr, failureMsg) :
  print("")
  print(cmdStr)
  print("")
  result = os.system(cmdStr)
  if result :
    print("=====================================================")
    print(f"ERROR: {failureMsg}")
    print(f"result: {result >> 8}")
    print("=====================================================")
    sys.exit(result >> 8)
