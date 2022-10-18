import sys
class CompileError(Error):
   def __init__ (self, error):
       super().__init__("CompileError: " + error); 
class SyntaxError(Error):
    def __init__ (self, error):
       super().__init__("SyntaxError: " + error);
class Error:
    def __init__(self, error) -> None:
        print(error)
        sys.exit(1)
