
import os
import yaml

def doPreTasks(config, configPath, baseDir) :
  print("------------------------------------------------")
  print("doing the pre tasks:")
  print("------------------------------------------------")

  if 'tagsDatabase' not in config : return

  tagsConfig = config['tagsDatabase']

  if 'localPath' not in tagsConfig : return

  localPath = tagsConfig['localPath']
  tagsDir = os.path.dirname(localPath)
  if not os.path.isdir(tagsDir) :

    if 'gitUrl' in tagsConfig :
      tagsBaseDir = os.path.dirname(tagsDir)
      tagsGitName = os.path.basename(tagsDir)
      os.makedirs(tagsBaseDir, exist_ok=True)
      os.chdir(tagsBaseDir)
      os.system("pwd")
      os.system(f"git clone {tagsConfig['gitUrl']} {tagsGitName}")
    else :
      os.makedirs(tagsDir, exist_ok=True)

  os.chdir(tagsDir)

  if 'remotePath' in tagsConfig :
    remotePath = tagsConfig['remotePath']
    os.system(f"rsync -av {remotePath} {localPath}")

  os.system(f"lgtExporter {configPath} {baseDir}")
