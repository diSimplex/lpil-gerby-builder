
import os
import yaml

def runATask(documentName, documentConfig, databaseConfig) :
  print("------------------------------------------------")
  print(f"running the task: {documentName}")
  print("------------------------------------------------")
  print(yaml.dump(documentConfig))
  print("------------------------------------------------")
  print(yaml.dump(databaseConfig))
  print("------------------------------------------------")

  taskDir = documentConfig['dir']
  if not os.path.isdir(taskDir) :
    taskBaseDir = os.path.dirname(taskDir)
    taskDirName = os.path.basename(taskDir)
    os.makedirs(taskBaseDir, exist_ok=True)
    os.chdir(os.path.dirname(taskDir))
    gitUrl = documentConfig['gitUrl']
    os.system(f"git clone {gitUrl} {taskDirName}")

  os.chdir(taskDir)

  print("git pull")
  os.system("git pull")

  docName = documentConfig['doc']
  cmd = f"lpilMagicRunner {docName} build/latex"
  print("--------------------")
  print(cmd)
  os.system(cmd)

  tagsPath = databaseConfig['localPath'].replace('.sqlite', '.tags')
  plastexDir = documentConfig['plastexDir']
  cmd = f"plastex --add-plugins --tags {tagsPath} --dir {plastexDir} {docName}"
  print("--------------------")
  print(cmd)
  os.system(cmd)
