import subprocess 

subprocess.run(['where','python'])

result = subprocess.run(['python','--version'], capture_output=True,encoding='UTF-8')
print(result.stdout)

subprocess.run(['dir','/A'], shell=True)