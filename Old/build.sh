pyinstaller --icon="Resources/cbIcon.ico" --onefile --log-level ERROR interpreter.py
mv ./dist/interpreter ./
rm -r ./dist
rm -r ./build
rm interpreter.spec
mv interpreter cbLang
