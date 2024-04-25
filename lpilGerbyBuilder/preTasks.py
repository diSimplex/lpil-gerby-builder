
import os
import yaml

def doPreTasks(config) :
  print("------------------------------------------------")
  print("doing the pre tasks:")
  print("------------------------------------------------")

  localPath = config['tags.localPath']
  tagsDir = os.path.dirname(localPath)
  if not os.path.isdir(tagsDir) :

    gitUrl = config['tags.gitUrl']
    if gitUrl :
      tagsBaseDir = os.path.dirname(tagsDir)
      tagsGitName = os.path.basename(tagsDir)
      os.makedirs(tagsBaseDir, exist_ok=True)
      os.chdir(tagsBaseDir)
      os.system("pwd")
      os.system(f"git clone {gitUrl} {tagsGitName}")
    else :
      os.makedirs(tagsDir, exist_ok=True)

  os.chdir(tagsDir)

  remotePath = config['tags.remotePath']
  if remotePath :
    os.system(f"rsync -av {remotePath} {localPath}")

  configPath = config['configPath']
  baseDir    = config['baseDir']
  os.system(f"lgtExporter {configPath} {baseDir}")
