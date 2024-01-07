#Native
import os.path
from os import name
import subprocess
import sys
import shutil

#PyPy
pyInstallerInstalled = True

try:
    import PyInstaller.__main__ as PyInstaller
except ImportError:
    pyInstallerInstalled = False

#Custom
from parse import Parser
from error import Error

version = "0.0.1"
prefix = ".exe" if name == "win32" else ""

class Interpreter:
    def Interpret(self, code : str) -> None:
        subprocess.call(["python", "output.py"])


def GetCode(filePath) -> str:
    if os.path.isfile(filePath):
        with open(filePath, 'r') as file:
            return file.read()
    else:
        Error("Input file not found")

def HandleArgs() -> None:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        Error('''
        Command line arguments:
        --help -h: Prints this message
        --version -b: Prints the version of the interpreter
        --run -r (default) [file]: Runs the interpreter on the file specified
        --transpile -t [file] [address]: Converts the file specified into python code and saves it to the address specified
        --compile -c [file] [address]: Compiles the file specified into an executable and saves it to the address specified
            ''')
    elif sys.argv[1] == "--run" or sys.argv[1] == "-r":
        if len(sys.argv) < 3:
            Error("Invalid number of arguments")
        else:
            if os.path.isfile(sys.argv[2]):
                parser = Parser(GetCode((sys.argv[2])))
                interpreter = Interpreter()
                interpreter.Interpret(parser.code)
            else:
                Error("File not found")
    elif os.path.isfile(sys.argv[1]):
        parser = Parser(GetCode(sys.argv[1]))
        interpreter = Interpreter()
        interpreter.Interpret(parser.code)
    elif sys.argv[1] == "--transpile" or sys.argv[1] == "-t":
        if len(sys.argv) < 4:
            Error("Invalid number of arguments")
        else:
            if os.path.isfile(sys.argv[2]):
                parser = Parser(GetCode((sys.argv[2])))
                with open(sys.argv[3], "w") as f:
                    f.write(parser.code)
            else:
                Error("Input file not found")
    elif sys.argv[1] == "--compile" or sys.argv[1] == "-c":
        if pyInstallerInstalled == False:
            Error("PyInstaller is not installed \n Please run \"pip install PyInstaller\"")
        if len(sys.argv) < 4:
            Error("Invalid number of arguments")
        else:
            if os.path.isfile(sys.argv[2]):
                parser = Parser(GetCode((sys.argv[2])))
                fileName = sys.argv[3].split(".")[0]
                with open(fileName + ".py", "w") as f:
                    f.write(parser.code)
                if (os.path.isfile(fileName+prefix)):
                    os.remove(fileName+prefix)
                subprocess.call(["PyInstaller", fileName + ".py", "--onefile"])
                os.rename("dist/{}".format(fileName+prefix), "./"+sys.argv[3])
                os.remove(fileName + ".py")
                os.remove(fileName + ".spec")
                shutil.rmtree("build")
                shutil.rmtree("dist")
            else:
                Error("File not found")
    else:
        Error("Invalid argument")

    if (os.path.isfile("output.py")):
        os.remove("output.py")

def CheckArgs() -> str:
    if len(sys.argv) < 2:
        Error("Invalid number of arguments")
    HandleArgs()
    
if __name__ == "__main__":
    CheckArgs()
