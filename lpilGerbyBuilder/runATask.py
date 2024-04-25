
import os
import yaml

def runATask(taskName, config) :
  print("------------------------------------------------")
  print(f"running the task: {taskName}")
  print("------------------------------------------------")
  print(yaml.dump(config[('documents', taskName)]))
  print("------------------------------------------------")

  taskDir = config[('documents', taskName, 'dir')]
  if not os.path.isdir(taskDir) :
    taskBaseDir = os.path.dirname(taskDir)
    taskDirName = os.path.basename(taskDir)
    os.makedirs(taskBaseDir, exist_ok=True)
    os.chdir(os.path.dirname(taskDir))
    gitUrl = config[('documents', taskName, 'gitUrl')]
    os.system(f"git clone {gitUrl} {taskDirName}")

  os.chdir(taskDir)
  os.system("git pull")

  docName = config[('documents', taskName, 'doc')]
  os.system(f"lpilMagicRunner {docName} build/latex")

  tagsPath = config['tags.localPath'].replace('.sqlite', '.tags')
  os.system(f"plastex --add-plugins --tags {tagsPath} {docName}")
