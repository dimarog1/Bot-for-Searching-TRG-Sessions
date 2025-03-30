class UserAlreadyExistsException(Exception):
    def __init__(self, message="Пользователь уже зарегистрирован"):
        self.message = message
        super().__init__(self.message)


class UserNotExistsException(Exception):
    def __init__(self, message="Пользователь не зарегистрирован"):
        self.message = message
        super().__init__(self.message)
