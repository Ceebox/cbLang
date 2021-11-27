pyinstaller --icon="Resources/cbIcon.ico" --onefile --log-level ERROR interpreter.py
move .\dist\interpreter.exe .\
@RD /S /Q .\dist
@RD /S /Q .\build
del cbLang.exe
del interpreter.spec
rename interpreter.exe cbLang.exe