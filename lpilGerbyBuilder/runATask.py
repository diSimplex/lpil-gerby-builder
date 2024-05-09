
import os
import yaml

from lpilGerbyBuilder.utils import ranCmd

def runATask(documentName, documentConfig, databaseConfig) :
  print("================================================")
  print(f"running the task: {documentName}")
  print("------------------------------------------------")
  print(yaml.dump(documentConfig))
  print("------------------------------------------------")
  print(yaml.dump(databaseConfig))
  print("------------------------------------------------")

  continueWithTask = True

  taskDir = documentConfig['dir']
  if not os.path.isdir(taskDir) :
    taskBaseDir = os.path.dirname(taskDir)
    taskDirName = os.path.basename(taskDir)
    os.makedirs(taskBaseDir, exist_ok=True)
    os.chdir(os.path.dirname(taskDir))
    gitUrl = documentConfig['gitUrl']
    continueWithTask = ranCmd(
      f"git clone {gitUrl} {taskDirName}",
      f"Could not clone {gitUrl}"
    )

  os.chdir(taskDir)

  if continueWithTask :
    continueWithTask = ranCmd("git pull", "Could not git pull")

  if continueWithTask :
    docName = documentConfig['doc']
    continueWithTask = ranCmd(
      f"lpilMagicRunner {docName} build/latex",
      f"Could not run lpilMagicRunner on {docName}"
    )

  if continueWithTask :
    tagsPath = databaseConfig['localPath'].replace('.sqlite', '.tags')
    plastexDir = documentConfig['plastexDir']
    continueWithTask = ranCmd(
      f"plastex --add-plugins --tags {tagsPath} --dir {plastexDir} {docName}",
      f"Could not run plastex on {docName}"
    )
