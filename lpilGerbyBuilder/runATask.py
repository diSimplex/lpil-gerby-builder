
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
  os.system("git pull")

  docName = documentConfig['doc']
  os.system(f"lpilMagicRunner {docName} build/latex")

  tagsPath = databaseConfig['localPath'].replace('.sqlite', '.tags')
  plastexDir = documentConfig['plastexDir']
  os.system(f"plastex --add-plugins --tags {tagsPath} --dir {plastexDir} {docName}")
