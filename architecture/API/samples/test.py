from decouple import config
import imp
print(config('TEST'))
name = 'TEST'   
if config('TEST') == 'ARGENTO':
    value = 'ORO'
else:
    value = 'ARGENTO' 
with open('.env', 'r', encoding='utf-8') as file:
    data = file.readlines()
edited = False
for line in data:
    if line.startswith(name):
        data.remove(line)
        break
line = name + "='" + value + "'\n"
data.append(line)
with open('.env', 'w', encoding='utf-8') as file:
    file.writelines(data)
print(config('TEST'))
from decouple import config
config = imp.reload(config)
print(config('TEST'))
