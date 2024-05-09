
import os
import subprocess
import sys
import yaml

def ranCmd(cmdStr, failureMsg, exitOnError=False) :
  print("")
  print(cmdStr)
  print("")
  cmdArray = cmdStr.split()
  #print(yaml.dump(cmdArray))
  result = subprocess.run(
    cmdArray,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
  )
  if result.returncode :
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(f"ERROR: {failureMsg}")
    print(f"result: {result.returncode >> 8}")
    if result.stdout : print(result.stdout.decode('utf-8'))
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    if exitOnError : sys.exit(result.returncode >> 8)
    else : return False
  else :
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(result.stdout.decode('utf-8'))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  return True