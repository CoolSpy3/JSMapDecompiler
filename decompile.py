import json
from pathlib import Path
import os
import re
import typing
import urllib.request

outputPath = str(Path('./output/').resolve()) + '/'

def safe_input(prompt: str, validResponses: typing.List[str]) -> str:
    res = None
    while res not in validResponses:
        res = input(prompt).lower()
        if res == 'exit':
            exit()
    return res

def formatFilePath(path: str) -> str:
    if path.startswith('webpack:///'):
        path = path[len('webpack:///'):]
    while path.startswith('.') or path.startswith('/'):
        path = path[1:]
    path_old = path
    path = re.sub(r'[^\/\\ a-zA-Z0-9_\-.]', '_', path)
    if path_old != path:
        print(f'Replacing: {path_old} with {path}')
    return str(outputPath + path)



os.system("clear")
print("       __ _____    __  ___                 ____                                        _  __")
print("      / // ___/   /  |/  /____ _ ____     / __ \ ___   _____ ____   ____ ___   ____   (_)/ /___   _____")
print(" __  / / \__ \   / /|_/ // __ `// __ \   / / / // _ \ / ___// __ \ / __ `__ \ / __ \ / // // _ \ / ___/")
print("/ /_/ / ___/ /  / /  / // /_/ // /_/ /  / /_/ //  __// /__ / /_/ // / / / / // /_/ // // //  __// /")
print("\____/ /____/  /_/  /_/ \__,_// .___/  /_____/ \___/ \___/ \____//_/ /_/ /_// .___//_//_/ \___//_/")
print("                             /_/                                           /_/                    ")
print("")

useDefaultOutput = safe_input('Do you want to specify the output directory [Y/N]: ', ['yes', 'no', 'y', 'n'])
if useDefaultOutput[0] == 'y':
	newOutputPath = input('Enter new Output Path: ')
	outputPath = str(Path(newOutputPath).resolve()) + '/'
	print(outputPath)

inputUri = input('Enter URI: ')
isFile = safe_input('Is this a file or a URL? [F/U]: ', ['file', 'url', 'f', 'u'])

isFile = isFile == 'f' or isFile == 'file'

if os.path.isdir(outputPath):
    cont = safe_input(f'{outputPath} already exists! Do you wish to continue? [Y/N]: ', ['yes','no','y','n'])
    if cont[0] == 'n':
        exit()

jsonText = None

if isFile:
    with open(inputUri, 'r') as file:
        jsonText = file.read()
else:
    with urllib.request.urlopen(inputUri) as url:
        jsonText = url.read().decode()

jsonObj = json.loads(jsonText)

if 'sources' not in jsonObj or 'sourcesContent' not in jsonObj:
    print('Source map does not contain "sources" and/or "sourcesContent" properties')

content = jsonObj['sourcesContent']

for idx, fp in enumerate(jsonObj['sources']):
    fp = formatFilePath(fp)
    try:
        if not os.path.exists(os.path.dirname(fp)):
            os.makedirs(os.path.dirname(fp))
        with open(fp, 'w') as file:
            file.write(content[idx])
    except Exception as e:
        print(f'Error Creating: {fp}')
        print(e)
