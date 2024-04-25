
import os
import yaml

def doPostTasks(config) :
  print("------------------------------------------------")
  print("doing the post tasks:")
  print("------------------------------------------------")

  gerbyDir = config['gerby.localPath']
  print(yaml.dump(gerbyDir))

  if not os.path.isdir(gerbyDir) :
    os.makedirs(gerbyDir, exist_ok=True)

  os.chdir(gerbyDir)

  for docName in config['documents'].keys() :
    origDir = os.path.join(
      config[('documents', docName, 'dir')],
      os.path.splitext(config[('documents', docName, 'doc')])[0]
    )
    os.system(f"rsync -av {origDir} {gerbyDir}")

  os.system("pwd")
  os.system("tree")
