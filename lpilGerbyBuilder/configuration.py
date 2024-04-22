
import os
import sys
import yaml

def malformedTask(aMessge, theTask) :
  print("Malformed task:")
  print(f"  {aMessage}")
  print("in the task definition:")
  print(yaml.dump(theTask))
  sys.exit(1)

def updatePath(aPath, baseDir) :
  aPath = aPath.replace('$baseDir', baseDir)
  return os.path.abspath(os.path.expanduser(
    aPath
  ))

def loadConfig(configPath, baseDir) :
  config = {}
  with open(configPath) as yamlFile :
    config = yaml.safe_load(yamlFile.read())

  if 'documents' not in config :
    print("No documents defined")
    print(" ... there is nothing to do...")
    sys.exit(1)

  baseDir = os.path.expanduser(baseDir)
  config['baseDir'] = baseDir

  if 'tagsDatabase' not in config :
    print("No tags database defined")
    print(" ... there is nothing to do...")
    sys.exit(1)

  tags = config['tagsDatabase']
  if 'localPath' not in tags :
    print("No local path to the tags database defined")
    print(" ... we can not proceed!")
    sys.exit(1)

  tags['localPath'] = updatePath(tags['localPath'], baseDir)
  if 'remotePath' in tags :
    tags['remotePath'] = updatePath(tags['remotePath'], baseDir)

  if 'gerbyWebsite' not in config :
    print("No geby website specified")
    print(" ... there is nothing to do...")
    sys.exit(1)

  gerby = config['gerbyWebsite']
  if 'localPath' not in gerby :
    print("No local path defined in the gerby website")
    print(" ... there is nothing to do...")
    sys.exit(1)

  gerby['localPath'] = updatePath(gerby['localPath'], baseDir)
  if 'remotePath' in gerby :
    gerby['remotePath'] = updatePath(gerby['remotePath'], baseDir)

  for aTask in config['documents'] :
    if 'dir' not in aTask    : malformedTask("no dir specified")
    if 'gitUrl' not in aTask : malformedTask("no gitUrl specified")
    if 'doc' not in aTask    : malformedTask("no doc specified")
    if '$baseDir' in aTask['dir'] :
      aTask['dir'] = updatePath(aTask['dir'], baseDir)
    if 'tagsPath' not in aTask :
      aTask['tagsPath'] = os.path.splitext(tags['localPath'])[0] + '.tags'

  return config
