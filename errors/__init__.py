class AppException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class BadRequest(AppException):
    status_code = 400

    def __init__(self, message: str):
        super().__init__(status_code=self.status_code, message=message)


class InternalServerError(AppException):
    status_code = 500

    def __init__(self):
        super().__init__(status_code=self.status_code, message='Internal server error!')


class NotFound(AppException):
    status_code = 404

    def __init__(self, message: str):
        super().__init__(status_code=self.status_code, message=message)


class Unauthorised(AppException):
    status_code = 401

    def __init__(self, message: str):
        super().__init__(status_code=self.status_code, message=message)
        