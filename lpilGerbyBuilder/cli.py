
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
  config = ConfigManager(
    chooseDatabase=True,
    chooseCollection=True,
    chooseDocument=True
  )
  config.loadConfig()
  config.checkInterface({
    'tags.databases.*.localPath' : {
      'msg' : 'Can not collect tags database if no localPath specified'
    },
    'gerby.collections.*.localPath' : {
      'msg' : 'Can not collect plastex output if no localPath specified'
    },
    'gerby.collections.*.documents.*.doc' : {
      'msg' : 'Documents MUST have a document specified'
    },
    'gerby.collections.*.documents.*.dir' : {
      'msg' : 'Documents MUST have a directory speficied'
    },
    'gerby.collections.*.documents.*.gitUrl' : {
      'msg' : 'Documents MUST have a git url speficied'
    },
    'gerby.collections.*.documents.*.plastexDir' : {
      'msg' : 'Documents MUST have a PlastTeX directory specified'
    },
    'gerby.collections.*.plastexDir' : {
      'msg' : 'Collections MUST have a PlasTex directory specified'
    },
  })

  doPreTasks(config)

  for aDatabaseName, aDatabaseConfig in config['tags.databases'].items() :
    if config.cmdArgs['database'] and \
      config.cmdArgs['database'] != aDatabaseName.lower() : continue
    for aCollectionName, aCollectionConfig in config['gerby.collections'].items() :
      if config.cmdArgs['collection'] and \
        config.cmdArgs['collection'] != aCollectionName.lower() : continue
      if aCollectionName.lower() == aDatabaseName.lower() :
        for aDocumentName, aDocumentConfig in aCollectionConfig['documents'].items() :
          if config.cmdArgs['document'] and \
            config.cmdArgs['document'] != aDocumentName.lower() : continue
          runATask(aDocumentName, aDocumentConfig, aDatabaseConfig)

  doPostTasks(config)
