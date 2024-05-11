
import os
import yaml

from lpilGerbyBuilder.utils import ranCmd

def doPostTasks(config) :
  print("================================================")
  print("doing the post tasks:")
  print("------------------------------------------------")


  for collectionName, collectionConfig in config['gerby.collections'].items() :
    if config.cmdArgs['collection'] and \
      config.cmdArgs['collection'] != collectionName.lower() : continue
    # we also enforce collectionName == databaseName
    # so do so here!
    if config.cmdArgs['database'] and \
      config.cmdArgs['database'] != collectionName.lower() : continue

    print(yaml.dump(collectionConfig))
    print("------------------------------------------------")

    continueWithTask = True

    gerbyDir = collectionConfig['plastexDir']
    print(yaml.dump(gerbyDir))

    if not os.path.isdir(gerbyDir) :
      os.makedirs(gerbyDir, exist_ok=True)

    os.chdir(gerbyDir)

    for documentName, documentConfig in collectionConfig['documents'].items() :
      if not continueWithTask : break
      origDir = documentConfig['plastexDir']
      gerbyDocDir = os.path.join(gerbyDir, 'html', 'docs', documentName)
      os.makedirs(gerbyDocDir, exist_ok=True)
      continueWithTask = ranCmd(
        f"rsync -av {origDir}/ {gerbyDocDir}",
        f"Could not rsync {origDir}/* to {gerbyDocDir}"
      )

    ranCmd("pwd", "Could not get the present working directory")
    ranCmd("tree", "Could not get the tree of this directory")

    if continueWithTask :
      #os.unlink(os.path.join(gerbyDir, 'db', f"{collectionName}.sqlite"))
      continueWithTask = ranCmd(
        f"gerbyCompiler --collection {collectionName} {' '.join(config.cmdArgs['configPaths'])}",
        f"Could not run gerbyCompiler on {collectionName}"
      )

    if continueWithTask :
      localPath = os.path.join(
        collectionConfig['localPath'],
        'gerbyWebsite',
      )
      remotePath = collectionConfig['remotePath']
      continueWithTask = ranCmd(
        f"rsync -av {localPath}/ {remotePath}",
        f"Could not rsync {localPath} to {remotePath}"
      )