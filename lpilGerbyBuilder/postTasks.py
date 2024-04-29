
import os
import yaml


def doPostTasks(config) :
  print("------------------------------------------------")
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

    gerbyDir = collectionConfig['plastexDir']
    print(yaml.dump(gerbyDir))

    if not os.path.isdir(gerbyDir) :
      os.makedirs(gerbyDir, exist_ok=True)

    os.chdir(gerbyDir)

    for documentName, documentConfig in collectionConfig['documents'].items() :
      origDir = documentConfig['plastexDir']
      gerbyDocDir = os.path.join(gerbyDir, 'html', documentName)
      os.makedirs(gerbyDocDir, exist_ok=True)
      os.system(f"rsync -av {origDir}/* {gerbyDocDir}")

    os.system("pwd")
    os.system("tree")

    os.system(f"gerbyCompiler --collection {collectionName} {' '.join(config.cmdArgs['configPaths'])}")
