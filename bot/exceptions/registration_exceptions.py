class UserAlreadyExistsException(Exception):
    def __init__(self, message="Пользователь уже зарегистрирован"):
        self.message = message
        super().__init__(self.message)
