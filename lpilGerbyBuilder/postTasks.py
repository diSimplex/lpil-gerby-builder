
import os
import yaml

def doPostTasks(config) :
  print("------------------------------------------------")
  print("doing the post tasks:")
  print("------------------------------------------------")
  print(yaml.dump(config))

  gerbyConfig = config['gerbyWebsite']

  gerbyDir = gerbyConfig['localPath']

  if not os.path.isdir(gerbyDir) :
    os.makedirs(gerbyDir, exist_ok=True)

  os.chdir(gerbyDir)
  os.system("pwd")
  os.system("tree")

  for aDocument in config['documents'] :
    #print(yaml.dump(aDocument))
    origDir = os.path.join(
      aDocument['dir'],
      os.path.splitext(aDocument['doc'])[0]
    )
    os.system(f"rsync -av {origDir} {gerbyDir}")

  os.system("pwd")
  os.system("tree")
