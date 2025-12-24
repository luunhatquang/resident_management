class BaseException(Exception):
    def __init__(self, message: str = "Error", code: int = 400, errors=None, status_code: int = 400):
        self.status_code = status_code
        self.message = message
        self.code = code
        self.errors = errors
        super().__init__(self.message)