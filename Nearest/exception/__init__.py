class Error(Exception):
    pass


class DalError(Error):
    pass


class DalEngineNotExistsError(DalError):
    def __init__(self, message):
        self.message = message
