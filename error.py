import sys
class Error():
    def __init__(self, error) -> None:
        print(error)
        sys.exit()