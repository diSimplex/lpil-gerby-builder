
import os
import yaml

def runATask(aTask) :
  print("------------------------------------------------")
  print("running the task:")
  print("------------------------------------------------")
  print(yaml.dump(aTask))

  taskDir = aTask['dir']
  if not os.path.isdir(taskDir) :
    taskBaseDir = os.path.dirname(taskDir)
    taskDirName = os.path.basename(taskDir)
    os.makedirs(taskBaseDir, exist_ok=True)
    os.chdir(os.path.dirname(taskDir))
    os.system(f"git clone {aTask['gitUrl']} {taskDirName}")

  os.chdir(taskDir)
  os.system("git pull")

  os.system(f"lpilMagicRunner {aTask['doc']} build/latex")
