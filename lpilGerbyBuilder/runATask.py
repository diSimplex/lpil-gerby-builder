
import os
import yaml

from lpilGerbyBuilder.utils import ranCmd

def runATask(
  documentName, documentConfig,
  collectionConfig, databaseConfig
) :
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

  plastexDir = documentConfig['plastexDir']
  if continueWithTask :
    tagsPath = databaseConfig['localPath'].replace('.sqlite', '.tags')
    continueWithTask = ranCmd(
      f"plastex --add-plugins --tags {tagsPath} --dir {plastexDir} {docName}",
      f"Could not run plastex on {docName}"
    )

  if continueWithTask :
    fileExtensions = [ '.pdf', '.bib', '.bbl']
    for anExt in fileExtensions :
      fileName = docName.replace('.tex','')+anExt
      filePath = os.path.join(taskDir, 'build', 'latex', fileName)
      if os.path.exists(filePath) :
        continueWithTask = ranCmd(
          f"cp {filePath} {plastexDir}/{fileName}",
          f"Could not copy the *{anExt} for {docName}"
        )

  gerbyDir = collectionConfig['plastexDir']
  if continueWithTask :
    gerbyDocDir = os.path.join(gerbyDir, 'html', 'docs', documentName)
    os.makedirs(gerbyDocDir, exist_ok=True)
    continueWithTask = ranCmd(
      f"rsync -av {plastexDir}/ {gerbyDocDir}",
      f"Could not rsync {plastexDir}/ to {gerbyDocDir}"
    )
