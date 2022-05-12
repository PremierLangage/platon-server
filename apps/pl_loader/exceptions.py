
class SyntaxErrorPL(Exception):
    """Raised when a syntax error occured while parsing a file."""
    
    
    def __init__(self, file_name, line, lineno, message="Syntax error"):
        self.file_name = file_name
        self.line = line
        self.message = message
        self.lineno = str(lineno)
    
    
    def __str__(self):
        return self.file_name + " - " + self.message + " at line " + str(
            self.lineno) + ":\n" + self.line



class SemanticError(Exception):
    """Raised when a semantic error occured while parsing a file."""
    
    
    def __init__(self, file_name, line, lineno, message="Semantic error"):
        self.file_name = file_name
        self.line = line
        self.message = message
        self.lineno = str(lineno)
    
    
    def __str__(self):
        return self.file_name + " -- " + self.message + " at line " + str(
            self.lineno) + "\n" + self.line

class ComponentNotFound(Exception):
    """Raised when a component cannot be found."""
    
    
    def __init__(self, component):
        self.component = component
        print('-----errr2-----')
    
    
    def __str__(self):
        return 'ComponentNotFound: component "%s" is not defined' \
               % (self.component)

class LoaderException(Exception):
    
    def __init__(self, error: str, status: int) -> None:
        self.error = error
        self.status = status
    

class LoaderInstenceException(LoaderException):

    def __init__(self, error: str, status: int) -> None:
        super().__init__(error, status)

class LoaderStateException(LoaderException):
    
    def __init__(self, error: str, status: int) -> None:
        super().__init__(error, status)
    

    