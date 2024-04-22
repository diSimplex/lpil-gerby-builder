
import os
import sys
import yaml

from lpilGerbyBuilder.configuration import loadConfig
from lpilGerbyBuilder.preTasks import doPreTasks
from lpilGerbyBuilder.postTasks import doPostTasks
from lpilGerbyBuilder.runATask import runATask

def usage() :
  print("""
lpilGerbyBuilder <<configPath>> <<baseDir>>

where:
  configPath   is a path to the lpilGerbyBuilder configurtion
  baseDir      is a path to the base directory of the whole build
""")
  sys.exit(1)

def cli() :
  if len(sys.argv) < 3 : usage()

  configPath = sys.argv[1]
  configPath = os.path.abspath(os.path.expanduser(configPath))

  baseDir    = sys.argv[2]
  config = loadConfig(configPath, baseDir)

#  doPreTasks(config, configPath, baseDir)

#  for aTask in config['documents'] :
#    runATask(aTask, config)

  doPostTasks(config)
