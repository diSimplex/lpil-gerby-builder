
import os
import sys
import yaml

from lpilGerbyConfig.config import ConfigManager
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

  config = ConfigManager(requireBaseDir=True)
  config.loadConfig()
  config.checkInterface({
    'tags.localPath' : {
      'msg' : 'Can not collect tags database if no localPath specified'
    },
    'gerby.localPath' : {
      'msg' : 'Can not collect plastex output if no localPath specified'
    },
    'documents.*.doc' : {
      'msg' : 'Documents MUST have a document specified'
    },
    'documents.*.dir' : {
      'msg' : 'Documents MUST have a directory speficied'
    },
    'documents.*.gitUrl' : {
      'msg' : 'Documents MUST have a git url speficied'
    }
  })

  doPreTasks(config)

  for aTask in config['documents'].keys() :
    runATask(aTask, config)

  doPostTasks(config)
