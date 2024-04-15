
import sys
import yaml

from lpilGerbyBuilder.configuration import loadConfig
from lpilGerbyBuilder.runATask import runATask

def usage() :
  print("lpilGerbyBuilder <<configPath>>")
  print("")
  print("configPath a path to the lpilGerbyBuilder configurtion")
  sys.exit(1)

def cli() :
  if len(sys.argv) < 2 : usage()

  config = loadConfig(sys.argv[1])

  for aTask in config['tasks'] :
    runATask(aTask)
