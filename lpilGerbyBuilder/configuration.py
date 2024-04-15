
import os
import sys
import yaml

def malformedTask(aMessge, theTask) :
  print("Malformed task:")
  print(f"  {aMessage}")
  print("in the task definition:")
  print(yaml.dump(theTask))
  sys.exit(1)

def loadConfig(configPath) :
  config = {}
  with open(configPath) as yamlFile :
    config = yaml.safe_load(yamlFile.read())

  if 'tasks' not in config :
    print("No tasks defined")
    print(" ... there is nothing to do...")
    sys.exit(1)

  baseDir = '~'
  if 'baseDir' in config : baseDir = config['baseDir']

  baseDir = os.path.expanduser(baseDir)
  config['baseDir'] = baseDir

  for aTask in config['tasks'] :
    if 'dir' not in aTask    : malformedTask("no dir specified")
    if 'gitUrl' not in aTask : malformedTask("no gitUrl specified")
    if 'doc' not in aTask    : malformedTask("no doc specified")
    if '$baseDir' in aTask['dir'] :
      aTask['dir'] = aTask['dir'].replace('$baseDir', baseDir)

  return config