
import os
import yaml

from lpilGerbyBuilder.utils import ranCmd

def doPreTasks(config) :
  print("================================================")
  print("DOING the PRE tasks:")
  #print(yaml.dump(config))
  print("------------------------------------------------")

  for aDatabaseName, aDatabase in config['tags.databases'].items() :
    if config.cmdArgs['database'] and \
      config.cmdArgs['database'] != aDatabaseName.lower() : continue
    localPath = aDatabase['localPath']
    print(f"working on: {aDatabaseName}")
    print(yaml.dump(aDatabase))
    print("------------------------------------------------")
    tagsDir = os.path.dirname(localPath)
    if not os.path.isdir(tagsDir) :

      gitUrl = aDatabase['gitUrl']
      if gitUrl :
        tagsBaseDir = os.path.dirname(tagsDir)
        tagsGitName = os.path.basename(tagsDir)
        os.makedirs(tagsBaseDir, exist_ok=True)
        os.chdir(tagsBaseDir)
        ranCmd("pwd", "Could not get 'pwd'")
        ranCmd(
          f"git clone {gitUrl} {tagsGitName}",
          f"Could not clone {gitUrl}"
        )
      else :
        os.makedirs(tagsDir, exist_ok=True)

    os.chdir(tagsDir)

    remotePath = aDatabase['remotePath']
    if remotePath :
      ranCmd(
        f"rsync -av {remotePath} {localPath}",
        f"Could not rsync {remotePath} to {localPath}"
      )

    configPaths = config['configPaths']
    ranCmd(
      f"lgtExporter --database={aDatabaseName} {' '.join(configPaths)}",
      f"Could not run lgtExporter",
      exitOnError=True)
    print("------------------------------------------------")
