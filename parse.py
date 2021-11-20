from error import Error

class Parser:
    def __init__(self, code: str):
        #Pass in code
        self.code = code
        #Parse code
        self.code = self.Parse(self.code)

    def Parse(self, code: str) -> str:
        #Parse code into normal python
        code = self.ParseInclude(code)
        code = self.ParseComments(code)
        code = self.ParseKeyWords(code)
        code = self.ParseEOL(code)
        code = self.ParseBraces(code)
        code = self.ParseFunctions(code)
        code = self.AddEntryPoint(code)

        #Dump code to file
        with open("output.py", "w") as f:
            f.write(code)
        return code

    def ParseComments(self, code: str) -> str:
        for line in code.splitlines():
            if "//" in line:
                if list(line)[0] == "/" and list(line)[1] == "/":
                    code = code.replace(line, "")
                else:
                    newLine = line.partition("//")[0]
                    code = code.replace(line, newLine)
        return code

    def ParseInclude(self, code: str) -> str:
        code = code.replace("from native reference", "import")
        includeName = ""
        for line in code.splitlines():
            if "from native include" in line:
                iterator = 0
                for word in line.split():
                    iterator += 1
                    if word == "include":
                        includeName = line.split()[iterator].replace(";", "")
                        code = code.replace(line, f"from {includeName} import *;")
        for line in code.splitlines():
            if "include" in line:
                iterator = 0
                for word in line.split():
                    iterator += 1
                    if word == "include":
                        includeName = line.split()[iterator].replace(";", "")
                        code = code.replace(line, "")
        with open(includeName + ".cb", "r") as file:
            code = code + "\n" + file.read()
        return code

    def ParseKeyWords(self, code: str) -> str:
        code = code.replace("this", "self")
        code = code.replace("true", "True")
        code = code.replace("false", "False")
        code = code.replace("null", "None")
        code = code.replace("else if", "elif")
        return code

    def ParseEOL(self, code: str) -> str:
        code = "".join([s for s in code.splitlines(True) if s.strip("\r\n")])

        for line in code.splitlines():
            skipLine = False
            for token in ["function", "while", "for", "if", "else", "elif"]:
                if token in line:
                    skipLine = True
            if ''.join(line.split()).startswith(("{", "}", "\n", "class")):
                skipLine = True
            elif line.strip() == "":
                skipLine = True
            if skipLine:
                continue
            if ";" in line:
                line = line.replace(";", "\n")
            elif line.endswith((":")):
                Error(f"Syntax error in: \n{line}")
            else:
                Error(f"Missing semicolon in: \n{line}")

        return code

    def ParseBraces(self, code: str) -> str:
        leftBracesAmount = code.count("{")
        rightBracesAmount = code.count("}")
        if leftBracesAmount != rightBracesAmount:
            Error(("Braces amount is not equal"))

        newCode = ""
        for line in code.splitlines():
            line = line.replace(";", "\n    ")
            if "class" in line:
                line = "\n"+" ".join(line.split())
            if "function" in line:
                line = "\n    "+" ".join(line.split())
            if ''.join(line.split()).startswith(("{")):
                newCode += ":\n"
            if "}" in line:
                line = line.replace("}", "")
            line = line.replace("{", "")
            newCode += line
            line += "\n"

        return newCode

    def ParseFunctions(self, code: str) -> str:
        code = code.replace("function", "def")
        code = code.replace("def Start", "def __init__")
        code = code.replace(") is", ") ->")
        for line in code.splitlines():
            if "def" in line:
                code = code.replace(line, line.replace("(", "(self,"))
        return code

    def AddEntryPoint(self, code: str) -> str:
        code += "\n"
        code += '''
if __name__ == "__main__":
    main = Main()
    main.Main()
        '''

        #Tidy code by removing empty lines
        code = "".join([s for s in code.splitlines(True) if s.strip("\t\r\n")])

        return code